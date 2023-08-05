import singer
from singer import utils
import snowflake.connector
from target_postgres import target_tools
from target_postgres.postgres import MillisLoggingConnection

from target_snowflake.snowflake import SnowflakeTarget

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
]


def main(config, input_stream=None):
    with snowflake.connector(
            connection_factory=MillisLoggingConnection,
            user=config.get('snowflake_user'),
            password=config.get('snowflake_password'),
            account=config.get('snowflake_account'),
            warehouse=config.get('snowflake_warehouse'),
            database=config.get('snowflake_database')
    ) as connection:
        target = SnowflakeTarget(
            connection,
            logging_level=config.get('logging_level'),
            default_column_length=config.get('default_column_length', 1000),
            persist_empty_tables=config.get('persist_empty_tables')
        )

        if input_stream:
            target_tools.stream_to_target(input_stream, target, config=config)
        else:
            target_tools.main(target)


def cli():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    main(args.config)
