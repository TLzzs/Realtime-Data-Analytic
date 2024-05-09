curl -XPUT -k 'https://127.0.0.1:9200/crime_records' \
  --header 'Content-Type: application/json' \
  --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "a40_abduction_and_related_offences": {
                "type": "integer"
            },
            "b30_burglary_break_and_enter": {
                "type": "integer"
            },
            "b30_burglary_break_and_enter":  {
                "type": "integer"
            },
            "a10_homicide_and_related_offences":{
                "type": "integer"
            },
            "f30_other_government_regulatory_offences":{
                "type": "integer"
            },
            "lga_code11":{
                "type": "text"
            },
            "total_division_c_offences": {
                "type": "integer"
            },
            "a30_sexual_offences": {
                "type": "integer"
            },
            "a70_stalking_harassment_and_threatening_behaviour": {
                "type": "integer"
            },
            "e10_justice_procedures": {
                "type": "integer"
            },
            "total_division_f_offences": {
                "type": "integer"
            },
            "a50_robbery": {
                "type": "integer"
            },
            "b50_deception": {
                "type": "integer"
            },
            "b20_property_damage": {
                "type": "integer"
            },
            "c30_drug_use_and_possession": {
                "type": "integer"
            },
            "total_division_a_offences": {
                "type": "integer"
            },
            "d30_public_nuisance_offences": {
                "type": "integer"
            },
            "reference_period": {
                "type": "text"
            },
            "b10_arson": {
                "type": "integer"
            },
            "total_division_d_offences": {
                "type": "integer"
            },
            "c20_cultivate_or_manufacture_drugs": {
                "type": "integer"
            },
            "f90_miscellaneous_offences": {
                "type": "integer"
            },
            "d20_disorderly_and_offensive_conduct": {
                "type": "integer"
            },
            "d40_public_security_offences": {
                "type": "integer"
            },
            "a80_dangerous_and_negligent_acts_endangering_people": {
                "type": "integer"
            },
            "total_division_b_offences": {
                "type": "integer"
            },
            "d10_weapons_and_explosives_offences": {
                "type": "integer"
            },
            "total_division_e_offences": {
                "type": "integer"
            },
            "e20_breaches_of_orders": {
                "type": "integer"
            },
            "f10_regulatory_driving_offences": {
                "type": "integer"
            },
            "a60_blackmail_and_extortion": {
                "type": "integer"
            },
            "b40_theft": {
                "type": "integer"
            },
            "c90_other_drug_offences": {
                "type": "integer"
            },
            "f20_transport_regulation_offences": {
                "type": "integer"
            },
            "a20_assault_and_related_offences": {
                "type": "integer"
            },
            "b60_bribery": {
                "type": "integer"
            },
            "c10_drug_dealing_and_trafficking": {
                "type": "integer"
            },
            "suburb_name": {
                "type": "text"
            }
        }
    }
}' \
  --user 'elastic:elastic' | jq '.'

        

        
       