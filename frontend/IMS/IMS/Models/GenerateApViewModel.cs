using System;
using IMS.Models;

namespace IMS.Models
{
    public class GenerateApViewModel
    {
        public DemandCreate Model { get; set; } = new DemandCreate();

        public GenerateApViewModel()
        {
            // Default values
            Model.fin_year = "2025-2026";
            Model.demand_type = "APD";
            Model.no_of_apd_demand_placed = 0;
        }

        // VALIDATION
        public bool IsValid()
        {
            if (string.IsNullOrWhiteSpace(Model.eqpt_code))
                return false;

            if (string.IsNullOrWhiteSpace(Model.eqpt_name))
                return false;

            if (string.IsNullOrWhiteSpace(Model.fin_year))
                return false;

            return true;
        }
    }
}
