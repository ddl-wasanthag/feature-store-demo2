# This is an example feature definition file for snowflake

from datetime import timedelta
from pathlib import Path

import pandas as pd

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    SnowflakeSource,
)
from feast.types import Float32, Int64

current = Path.cwd()


# Sources are queried when building training datasets or materializing features into an online store.
# Read form snowflake

driver_stats_source = SnowflakeSource(
    database='FEAST', 
    table='DRIVER_STATS',
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
) 

# Define an entity for the driver. You can think of an entity as a primary key
# used to fetch features.
driver = Entity(
    name="driver",
    join_keys=["driver_id"],
    description="driver id",
)

# Our parquet files contain sample data that includes a driver_id column, timestamps and
# three feature column. Here we define a Feature View that will allow us to serve this
# data to our model online.
driver_stats_fv = FeatureView(
    # The unique name of this feature view. Two feature views in a single
    # project cannot have the same name
    name="driver_hourly_stats",

    entities=[driver],
    ttl=timedelta(days=1),
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    online=True,
    source=driver_stats_source,
    # Tags are user defined key/value pairs that are attached to each
    # feature view
    tags={"team": "driver_performance"},
)