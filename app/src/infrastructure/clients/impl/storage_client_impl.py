from typing import List

import boto3
from botocore.exceptions import ClientError
from pydantic.v1 import ValidationError

from src.application.clients.interface.file_writer_interface import FileWriterInterface
from src.application.exceptions.failed_save_data_exception import FailedSaveDataException
from src.application.logging.logger_interface import LoggerInterface
from src.domain.models.bank_model import BankModel
from src.domain.models.metadata_model import MetadataModel
from src.infrastructure.mappers.dto_mapper import bank_model_list_and_metadata_to_save_data_request_dto


class FileWriterImpl(FileWriterInterface):
    CONTENT_TYPE = "application/json"
    S3_BUCKET_NAME = "my-bucket-name"
    OBJECT_KEY = "BankList/data.json"

    def __init__(self, logger: LoggerInterface):
        self.__logger = logger

    def write_certificate_file(self, metadata: MetadataModel, items: List[BankModel]):
        try:
            request_dto = bank_model_list_and_metadata_to_save_data_request_dto(metadata, items)
            data_json = request_dto.model_dump_json()

            s3_client = boto3.client('s3')

            s3_client.put_object(
                Bucket=self.S3_BUCKET_NAME,
                Key=self.OBJECT_KEY,
                Body=data_json,
                ContentType=self.CONTENT_TYPE
            )

        except (ClientError, ValueError, ValidationError) as ex:
            self.__logger.error(
                f"[StorageClientImpl] Error saving data to s3 bucket. Exception: {ex}"
            )
            raise FailedSaveDataException
