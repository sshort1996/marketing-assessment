CREATE OR REPLACE PROCEDURE ASSESSMENT.TRF.DEDUPE_TO_TRF_PROC(
    TABLE_NAME STRING,
    ID_COLUMN_NAME STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    TRF_TABLE_NAME STRING;
BEGIN
    -- Construct the full table names
    TRF_TABLE_NAME := CONCAT('ASSESSMENT.TRF.', REPLACE(TABLE_NAME, 'RAW', 'TRF'));
    TABLE_NAME := CONCAT('ASSESSMENT.RAW.', TABLE_NAME);

    -- Insert deduplicated data into the existing TRF table without replacing it
    EXECUTE IMMEDIATE '
        INSERT INTO ' || TRF_TABLE_NAME || '
        SELECT * FROM (
            SELECT *, 
                   ROW_NUMBER() OVER (PARTITION BY ' || ID_COLUMN_NAME || ' ORDER BY ' || ID_COLUMN_NAME || ') AS RN
            FROM ' || TABLE_NAME || '
        ) AS deduped_table
        WHERE RN = 1
    ';

    RETURN 'Deduplication complete. Data inserted into: ' || TRF_TABLE_NAME;
END;
$$;
