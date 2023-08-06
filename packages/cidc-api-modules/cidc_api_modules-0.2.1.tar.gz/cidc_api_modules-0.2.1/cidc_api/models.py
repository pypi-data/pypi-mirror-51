import os
import hashlib
from functools import wraps
from typing import BinaryIO, Optional

from flask import current_app as app
from google.cloud.storage import Blob
from sqlalchemy import (
    Column,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    VARCHAR,
    Enum,
    Index,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from cidc_schemas import prism

## Constants
ORGS = ["CIDC", "DFCI", "ICAHN", "STANFORD", "ANDERSON"]
ROLES = [
    "cidc-admin",
    "cidc-biofx-user",
    "cimac-biofx-user",
    "cimac-user",
    "developer",
    "devops",
    "nci-biobank-user",
]

# See: https://github.com/CIMAC-CIDC/cidc-schemas/blob/master/cidc_schemas/schemas/artifacts/artifact_core.json
ARTIFACT_CATEGORIES = [
    "Assay Artifact from CIMAC",
    "Pipeline Artifact",
    "Manifest File",
    "Other",
]
ASSAY_CATEGORIES = [
    "Whole Exome Sequencing (WES)",
    "RNASeq",
    "Conventional Immunohistochemistry",
    "Multiplex Immunohistochemistry",
    "Multiplex Immunofluorescence",
    "CyTOF",
    "OLink",
    "NanoString",
    "ELISpot",
    "Multiplexed Ion-Beam Imaging (MIBI)",
    "Other",
    "None",
]
FILE_TYPES = [
    "FASTA",
    "FASTQ",
    "TIFF",
    "VCF",
    "TSV",
    "Excel",
    "NPX",
    "BAM",
    "MAF",
    "PNG",
    "JPG",
    "XML",
    "Other",
]
## End constants


def get_DOMAIN() -> dict:
    """
    Render all cerberus domains for data model resources 
    (i.e., any model extending `CommonColumns`).
    """
    domain_config = {}
    domain_config["new_users"] = ResourceConfig(Users)
    domain_config["trial_metadata"] = ResourceConfig(TrialMetadata, id_field="trial_id")
    for model in [Users, UploadJobs, Permissions, DownloadableFiles]:
        domain_config[model.__tablename__] = ResourceConfig(model)

    # Eve-sqlalchemy needs this to be specified explicitly for foreign key relations
    related_resources = {
        (Permissions, "to_user"): "users",
        (Permissions, "by_user"): "users",
        (Permissions, "trial"): "trial_metadata",
        (UploadJobs, "uploader"): "users",
        (DownloadableFiles, "trial"): "trial_metadata",
    }

    domain = DomainConfig(domain_config, related_resources).render()

    # Restrict operations on the 'new_users' resource
    del domain["new_users"]["schema"]["role"]
    del domain["new_users"]["schema"]["approval_date"]
    domain["new_users"]["item_methods"] = []
    domain["new_users"]["resource_methods"] = ["POST"]

    # Make downloadable_files read-only
    domain["downloadable_files"]["allowed_methods"] = ["GET"]
    domain["downloadable_files"]["allowed_item_methods"] = ["GET"]

    # Add the download_link field to the downloadable_files schema
    domain["downloadable_files"]["schema"]["download_link"] = {"type": "string"}

    return domain


def make_etag(*args):
    """Make an _etag by stringify, concatenating, and hashing the provided args"""
    argstr = "|".join([str(arg) for arg in args])
    argbytes = bytes(argstr, "utf-8")
    return hashlib.md5(argbytes).hexdigest()


def with_default_session(f):
    """
    For some `f` expecting a database session instance as a keyword argument,
    set the default value of the session keyword argument to the current app's
    database driver's session. We need to do this in a decorator rather than
    inline in the function definition because the current app is only available
    once the app is running and an application context has been pushed.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if "session" not in kwargs:
            kwargs["session"] = app.data.driver.session
        return f(*args, **kwargs)

    return wrapped


BaseModel = declarative_base()


class CommonColumns(BaseModel):
    """Metadata attributes that Eve uses on all resources"""

    __abstract__ = True  # Indicate that this isn't a Table schema

    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    @classmethod
    @with_default_session
    def find_by_id(cls, id: int, session: Session):
        """Find the record with this id"""
        return session.query(cls).get(id)


class Users(CommonColumns):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    first_n = Column(String)
    last_n = Column(String)
    organization = Column(Enum(*ORGS, name="orgs"))
    approval_date = Column(DateTime)
    role = Column(Enum(*ROLES, name="role"))
    disabled = Column(Boolean, default=False, server_default="false")

    @staticmethod
    @with_default_session
    def find_by_email(email: str, session: Session) -> Optional:
        """
            Search for a record in the Users table with the given email.
            If found, return the record. If not found, return None.
        """
        user = session.query(Users).filter_by(email=email).first()
        return user

    @staticmethod
    @with_default_session
    def create(profile: dict, session: Session):
        """
            Create a new record for a user if one doesn't exist
            for the given email. Return the user record associated
            with that email.
        """
        email = profile.get("email")
        first_n = profile.get("given_name")
        last_n = profile.get("family_name")

        user = Users.find_by_email(email)
        if not user:
            app.logger.info(f"Creating new user with email {email}")
            user = Users(email=email)
            session.add(user)
            session.commit()
        return user


class Permissions(CommonColumns):
    __tablename__ = "permissions"

    # If user who granted this permission is deleted, this permission will be deleted.
    # TODO: is this what we want?
    granted_by_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    by_user = relationship("Users", foreign_keys=[granted_by_user])
    granted_to_user = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    to_user = relationship("Users", foreign_keys=[granted_to_user])

    trial_id = Column(
        String,
        ForeignKey("trial_metadata.trial_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trial = relationship("TrialMetadata", foreign_keys=[trial_id])

    assay_type = Column(Enum(*ASSAY_CATEGORIES, name="assays"), nullable=False)
    mode = Column(Enum("read", "write", name="mode"))


class TrialMetadata(CommonColumns):
    __tablename__ = "trial_metadata"
    # The CIMAC-determined trial id
    trial_id = Column(String, unique=True, nullable=False, index=True)
    metadata_json = Column(JSONB, nullable=False)

    # Create a GIN index on the metadata JSON blobs
    _metadata_idx = Index("metadata_idx", metadata_json, postgresql_using="gin")

    @staticmethod
    @with_default_session
    def find_by_trial_id(trial_id: str, session: Session):
        """
            Find a trial by its CIMAC id.
        """
        return session.query(TrialMetadata).filter_by(trial_id=trial_id).first()

    @staticmethod
    @with_default_session
    def patch_trial_metadata(trial_id: str, metadata: dict, session: Session):
        """
            Applies updates to an existing trial metadata record,
            or create a new one if it does not exist.

            Args:
                trial_id: the lead organization study id for this trial
                metadata: a partial metadata object for trial_id

            TODO: implement metadata merging, either here or in cidc_schemas
        """
        # Look for an existing trial
        trial = TrialMetadata.find_by_trial_id(trial_id, session=session)

        if trial:
            # Merge-update metadata into existing trial's metadata_json
            updated_metadata = prism.merge_clinical_trial_metadata(
                metadata, trial.metadata_json
            )
            # Save updates to trial record
            session.query(TrialMetadata).filter_by(trial_id=trial.trial_id).update(
                {
                    "metadata_json": updated_metadata,
                    "_etag": make_etag(trial.trial_id, updated_metadata),
                }
            )
            session.commit()
        else:
            # Create a new trial metadata record, since none exists
            app.logger.info(f"Creating new trial_metadata for trial {trial_id}")
            new_trial = TrialMetadata(trial_id=trial_id, metadata_json=metadata)
            session.add(new_trial)
            session.commit()


STATUSES = ["started", "completed", "errored"]


class UploadJobs(CommonColumns):
    __tablename__ = "upload_jobs"
    # The current status of the upload job
    status = Column(Enum(*STATUSES, name="job_statuses"), nullable=False)
    # The object names for the files to be uploaded
    gcs_file_uris = Column(ARRAY(String, dimensions=1), nullable=False)
    # TODO: track the GCS URI of the .xlsx file used for this upload
    # gcs_xlsx_uri = Column(String, nullable=False)
    # The parsed JSON metadata blob associated with this upload
    metadata_json_patch = Column(JSONB, nullable=False)
    # Link to the user who created this upload job
    uploader_email = Column(String, ForeignKey("users.email", onupdate="CASCADE"))
    uploader = relationship("Users", foreign_keys=[uploader_email])
    # A type of assay (wes, olink, ...) this upload is related to
    assay_type = Column(String, nullable=False)

    # Create a GIN index on the GCS object names
    _gcs_objects_idx = Index("gcs_objects_idx", gcs_file_uris, postgresql_using="gin")

    @staticmethod
    @with_default_session
    def create(
        assay_type: str,
        uploader_email: str,
        gcs_file_uris: list,
        metadata: dict,
        session: Session,
    ):
        """Create a new upload job for the given trial metadata patch."""
        job = UploadJobs(
            assay_type=assay_type,
            gcs_file_uris=gcs_file_uris,
            metadata_json_patch=metadata,
            uploader_email=uploader_email,
            status="started",
            _etag=make_etag(
                assay_type, gcs_file_uris, metadata, uploader_email, "started"
            ),
        )
        session.add(job)
        session.commit()

        return job


class DownloadableFiles(CommonColumns):
    """
    Store required fields from: 
    https://github.com/CIMAC-CIDC/cidc-schemas/blob/master/cidc_schemas/schemas/artifacts/artifact_core.json
    """

    __tablename__ = "downloadable_files"

    file_name = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    uploaded_timestamp = Column(DateTime, nullable=False)
    artifact_category = Column(
        Enum(*ARTIFACT_CATEGORIES, name="artifact_category"), nullable=False
    )
    assay_type = Column(String, nullable=False)
    md5_hash = Column(String, nullable=False)
    trial_id = Column(String, ForeignKey("trial_metadata.trial_id"), nullable=False)
    trial = relationship(TrialMetadata, foreign_keys=[trial_id])
    object_url = Column(String, nullable=False)
    visible = Column(Boolean, default=True)

    @staticmethod
    @with_default_session
    def create_from_metadata(
        trial_id: str, assay_type: str, file_metadata: dict, session: Session
    ):
        """
        Create a new DownloadableFiles record from a GCS blob.
        """
        etag = make_etag(*(file_metadata.values()))

        # Filter out keys that aren't columns
        supported_columns = DownloadableFiles.__table__.columns.keys()
        filtered_metadata = {"trial_id": trial_id, "assay_type": assay_type}
        for key, value in file_metadata.items():
            if key in supported_columns:
                filtered_metadata[key] = value
        # TODO maybe put non supported stuff from file_metadata to some misc jsonb column?

        new_file = DownloadableFiles(_etag=etag, **filtered_metadata)
        session.add(new_file)
        session.commit()
