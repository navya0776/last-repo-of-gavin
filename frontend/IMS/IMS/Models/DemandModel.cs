using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Models
{
    public class DemandModel
    {
        public class DmdJunctionCreate
        {
            public string Page_no { get; set; }
            public int demand_no { get; set; }
            public bool is_locked { get; set; }

            public string Scale_no { get; set; }
            public string Part_no { get; set; }
            public string Nomenclature { get; set; }
            public string A_u { get; set; }
            public int Auth { get; set; }
            public int Curr_stk_bal { get; set; }
            public int Dues_in { get; set; }
            public int Outs_Reqd { get; set; }

            public int stk_N_yr { get; set; } = 0;
            public int Reqd_as_OHS { get; set; } = 0;
            public string Cons_pattern { get; set; } = "0/0";
            public int qty_dem { get; set; } = 0;
            public int Recd { get; set; } = 0;

            public string Dept_ctrl { get; set; } = "0";
            public string? Dept_ctrl_dt { get; set; }

            public string eqpt_code { get; set; }  // EXTRA FIELD
        }

        public class LedgerResponse
        {
            public string ledger_code { get; set; }
            public string ledger_name { get; set; }
            public string eqpt_code { get; set; }
            public string eqpt_name { get; set; }
        }
        public class DmdJunctionResponse
        {
            public string Page_no { get; set; }
            public string Scale_no { get; set; }
            public string Part_no { get; set; }
            public string Nomenclature { get; set; }
            public string A_u { get; set; }
            public int Auth { get; set; }
            public int Curr_stk_bal { get; set; }
            public int Dues_in { get; set; }
            public int Outs_Reqd { get; set; }

            public int stk_N_yr { get; set; }
            public int Reqd_as_OHS { get; set; }
            public string Cons_pattern { get; set; }
            public int qty_dem { get; set; }
            public int Recd { get; set; }

            public string Dept_ctrl { get; set; }
            public string Dept_ctrl_dt { get; set; }

            public string eqpt_code { get; set; }
            public int demand_no { get; set; }
        }

        public class DemandResponse
        {
            public int demand_no { get; set; }
            public string eqpt_code { get; set; }
            public string equipment { get; set; }
            public int no_equipment { get; set; }
            public string fin_year { get; set; }
            public string demand_type { get; set; }
            public int demand_auth { get; set; }
            public int full_received { get; set; }
            public int part_received { get; set; }
            public int outstanding { get; set; }
            public float percent_received { get; set; }
        }

    }
}
