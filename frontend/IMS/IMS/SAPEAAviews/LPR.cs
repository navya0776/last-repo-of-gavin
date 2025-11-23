using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;



namespace IMS.SAPEAAviews
{
    public class LPRItem
    {
        public int Srl { get; set; }
        public string Lpr_No { get; set; }
        public DateTime Date { get; set; }
        public string Indent_No { get; set; }
        public string Job_No_Comp_Dt { get; set; }
        public string Ohs { get; set; }
        public string Page { get; set; }
        public string Part_No { get; set; }
        public string Nomen { get; set; }
        public int Qty { get; set; }
        public int Recd { get; set; }
        public string So { get; set; }
        public DateTime? So_Date { get; set; }
        public string Vend { get; set; }
        public double Rate { get; set; }
        public string Status { get; set; }
    }


    public class ShortOrderItem
    {
        public int Srl { get; set; }
        public string Lpr_No { get; set; }
        public string Date { get; set; }
        public string Indent_No { get; set; }
        public string Job_No_Comp_Dt { get; set; }
        public string Ohs { get; set; }
        public string Page { get; set; }
        public string Part_No { get; set; }
        public string Nomen { get; set; }
        public int Qty { get; set; }
        public int Recd { get; set; }
        public string So { get; set; }
        public string So_Date { get; set; }
        public string Vend { get; set; }
        public string Rate { get; set; }
        public string Status { get; set; }
    }
}
