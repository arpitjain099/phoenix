"""Constants for pipeline jobs."""


GATHER_BATCHES_TABLE_NAME = "gather_batches"
GENERALISED_MESSAGES_TABLE_NAME = "generalised_messages"
DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME = "deduped_generalised_messages"
DEDUPLICATED_GENERALISED_AUTHORS_TABLE_NAME = "deduped_generalised_authors"
CLASSIFIED_MESSAGES_TABLE_NAME = "classified_messages"
TABULATED_MESSAGES_TABLE_NAME = "tabulated_messages"
MANUALLY_CLASSIFIED_AUTHORS_TABLE_NAME = "manually_classified_authors"
# We are going for 2,000 as there is a limit of 1500 load jobs in a 24 hour period for Big Query,
# This will mean that most gathers will have a max a handful of load jobs.
# Furthermore there is a limit of 10MB per row. The hope is that 2000 batch size will keep the
DEFAULT_BATCH_SIZE = 2000
