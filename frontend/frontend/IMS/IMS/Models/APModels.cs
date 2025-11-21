using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Models
{
    internal class APModels
    {
        public class AP_Demand
        {
            public string equipment_code { get; set; }
            public string equipment_name { get; set; }
            public string demand_type { get; set; }
            public int quantity { get; set; }
        }
        public class Demand_Details
        {
            public int sub_dem_no { get; set; }
            public string status { get; set; }
            public int received { get; set; }
            public string remarks { get; set; }
        }
    }
}
