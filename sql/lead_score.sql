-- Lead score in SQL (DuckDB)
--
-- Scores every lead in data/leads.csv with the final logistic regression
-- from notebooks/lead_scoring_case_study.ipynb, so the model can run inside a
-- warehouse or CRM without Python.
--
-- The coefficients and the scaler mean/std for "Total Time Spent on Website"
-- come from the trained model (training split, random_state=100). The cleaning
-- steps repeat the notebook's logic for the 11 features the model uses.
--
-- Run from the repo root:
--   duckdb -c ".read sql/lead_score.sql"

WITH raw AS (
    SELECT * FROM read_csv('data/leads.csv', header = true)
),

-- Outlier bounds (IQR) computed on the full dataset, as in the notebook
time_bounds AS (
    SELECT
        quantile_cont("Total Time Spent on Website", 0.25) AS q1,
        quantile_cont("Total Time Spent on Website", 0.75) AS q3
    FROM raw
),

cleaned AS (
    SELECT
        r."Prospect ID" AS prospect_id,
        r."Converted" AS converted,
        r."Lead Origin" AS lead_origin,
        -- Blank lead source is imputed as Google, as in the notebook
        lower(coalesce(r."Lead Source", 'Google')) AS lead_source,
        -- Blank last activity is imputed as the most common value
        CASE
            WHEN r."Last Activity" IS NULL THEN 'Email Opened'
            WHEN r."Last Activity" IN (
                'Unreachable', 'Unsubscribed', 'Had a Phone Conversation',
                'Approached upfront', 'View in browser link Clicked',
                'Email Marked Spam', 'Email Received',
                'Visited Booth in Tradeshow', 'Resubscribed to emails'
            ) THEN 'Others'
            ELSE r."Last Activity"
        END AS last_activity,
        -- "Select" means the form field was left blank
        CASE
            WHEN r."Specialization" IS NULL OR r."Specialization" = 'Select' THEN 'Others'
            ELSE r."Specialization"
        END AS specialization,
        r."What is your current occupation" AS occupation,
        -- Cap and floor at 1.5 x IQR
        least(
            greatest(r."Total Time Spent on Website", b.q1 - 1.5 * (b.q3 - b.q1)),
            b.q3 + 1.5 * (b.q3 - b.q1)
        ) AS time_on_site
    FROM raw AS r
    CROSS JOIN time_bounds AS b
),

log_odds AS (
    SELECT
        prospect_id,
        converted,
        -1.1624534043960737
        + 1.052743682008061   * ((time_on_site - 483.8758503401361) / 546.5234096048471)
        - 1.25247804133947    * (lead_origin = 'Landing Page Submission')::INT
        + 0.8477410092271008  * (lead_source = 'olark chat')::INT
        + 2.9395604482316253  * (lead_source = 'reference')::INT
        + 5.435592015134097   * (lead_source = 'welingak website')::INT
        + 1.0931915339245943  * (last_activity = 'Email Opened')::INT
        + 1.3971120590868025  * (last_activity = 'Others')::INT
        + 2.2001305908130844  * (last_activity = 'SMS Sent')::INT
        - 1.1000721298444915  * (specialization = 'Hospitality Management')::INT
        - 1.221745888089746   * (specialization = 'Others')::INT
        + 2.6849663671936255  * (coalesce(occupation = 'Working Professional', false))::INT
        AS z
    FROM cleaned
)

SELECT
    prospect_id,
    converted,
    1 / (1 + exp(-z)) AS converted_prob,
    round(100 / (1 + exp(-z)))::INT AS lead_score,
    CASE
        WHEN round(100 / (1 + exp(-z))) >= 70 THEN 'Hot'
        WHEN round(100 / (1 + exp(-z))) >= 35 THEN 'Warm'
        ELSE 'Cold'
    END AS lead_bucket
FROM log_odds
ORDER BY lead_score DESC;
