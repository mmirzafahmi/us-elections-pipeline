WITH raw_schedulea AS (
    SELECT * FROM {{ source('virginia_elections', 'schedule_a') }}
)
SELECT
    ReportId,
    CommitteeContactId,
    FirstName
FROM raw_schedulea