"""Constants for pipeline jobs."""


GATHER_BATCHES_TABLE_NAME = "gather_batches"
GENERALISED_MESSAGES_TABLE_NAME = "generalised_messages"
DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME = "deduped_generalised_messages"
CLASSIFIED_MESSAGES_TABLE_NAME = "classified_messages"
TABULATED_MESSAGES_TABLE_NAME = "tabulated_messages"
MANUALLY_CLASSIFIED_AUTHORS_TABLE_NAME = "manually_classified_authors"
# We are going for 10,000 as there is a limit of 1500 load jobs in a 24 hour period for Big Query,
# This will mean that most gathers will have a max a handful of load jobs.
DEFAULT_BATCH_SIZE = 10000
