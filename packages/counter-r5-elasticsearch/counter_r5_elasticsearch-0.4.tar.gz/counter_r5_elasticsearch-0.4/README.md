Django project to generate 
[Counter R5](https://www.projectcounter.org/code-of-practice-five-sections/abstract/) 
reports using an elasticsearch index that stores usage transactions using
a predefined [JSON schema](schemas/counter_r5_transaction.schema.json) and elasticsearch 
[mapping](schemas/elasticsearch_mapping.json).

# Command line interface

Use `generate_csv_report` to generate R5 reports from an elasticsearch index.

CSV data will be output to `stdout`.

Example:

    python generate_csv_report.py --esindex "counter_r5" --begin_date "2017-01-01" --end_date "2019-01-01" --customer_id "univlaval" --customer_name "universite laval" --with_breakdown_by_month 1

Usage:

    --eshost                    Elasticsearch host (default: localhost)
    --esport                    Elasticsearch port (default: 9200)
    --esindex                   Elasticsearch index name
    --begin_date                Report begin date (YYYY-MM-DD)
    --end_date                  Report end date (YYYY-MM-DD)
    --customer_id               Id of the institution the report is for
    --customer_name             Name of the institution the report is for
    --with_breakdown_by_month   Append number of access by month columns (0/1) 
                                    (default: 0)
    --report_type               Only TR_J1 is supported (default: TR_J1)
