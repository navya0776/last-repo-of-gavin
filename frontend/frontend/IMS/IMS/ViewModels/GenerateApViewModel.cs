using System;
using static IMS.Models.DemandModel;

namespace IMS.Windows
{
    public class GenerateApViewModel
    {
        public DmdJunctionCreate Model { get; set; }

        public GenerateApViewModel()
        {
            Model = new DmdJunctionCreate();
        }

        // Basic validation
        public bool IsValid()
        {
            return !string.IsNullOrWhiteSpace(Model.Page_no)
                && !string.IsNullOrWhiteSpace(Model.eqpt_code)
                && Model.Auth >= 0;
        }
    }
}
