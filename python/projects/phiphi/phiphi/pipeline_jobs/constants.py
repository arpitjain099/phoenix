"""Constants for pipeline jobs."""


GATHER_BATCHES_TABLE_NAME = "gather_batches"
# We had a problem with the limit and had to change the name of the table so we could still process
# the recompute on the same day.
# Once the migrations is complete this should be change back to `generalised_messages`.
GENERALISED_MESSAGES_TABLE_NAME = "generalised_messages_tmp2"
DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME = "deduped_generalised_messages"
CLASSIFIED_MESSAGES_TABLE_NAME = "classified_messages"
TABULATED_MESSAGES_TABLE_NAME = "tabulated_messages"
MANUALLY_CLASSIFIED_AUTHORS_TABLE_NAME = "manually_classified_authors"
# We are going for 2,000 as there is a limit of 1500 load jobs in a 24 hour period for Big Query,
# This will mean that most gathers will have a max a handful of load jobs.
# Furthermore there is a limit of 10MB per row. The hope is that 2000 batch size will keep the
DEFAULT_BATCH_SIZE = 2000
