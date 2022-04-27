from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv, combine_codelists, filter_codes_by_category # NOQA

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.all(),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    age=patients.age_as_of(
        "2019-09-01",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    bmi=patients.most_recent_bmi(
        between=["2010-02-01", "2020-01-31"],
        minimum_age_at_measurement=18,
        include_measurement_date=True,
        date_format="YYYY-MM",
        return_expectations={
            "date": {"earliest": "2019-01-01", "latest": "2020-12-31"},
            "float": {"distribution": "normal", "mean": 28, "stddev": 8},
            "incidence": 0.80,
        }
    ),
    gp_count=patients.with_gp_consultations(
        between=["2019-01-01", "2020-12-31"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 6, "stddev": 3},
            "incidence": 0.6,
        },
    ),
    flu_vaccine=patients.with_tpp_vaccination_record(
        target_disease_matches="influenza",
        between=["2019-01-01", "2020-12-31"],
        returning="date",
        date_format="YYYY-MM",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": "2019-09-01", "latest": "2020-03-29"}
        }
    ),
)
