
  
    
    
    
        
         


        insert into `default`.`stg_schedulea__dbt_backup`
        ("ReportId", "CommitteeContactId", "FirstName")WITH raw_schedulea AS (
    SELECT * FROM `default`.`schedule_a`
)
SELECT
    ReportId,
    CommitteeContactId,
    FirstName
FROM raw_schedulea
  