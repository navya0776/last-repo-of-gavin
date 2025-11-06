using DocumentFormat.OpenXml.Office2016.Drawing.Command;
using System;

namespace IMS.Models
{
    // Ledger model containing all requested fields (C: keep all and add missing ones)
    public class LedgerItem
    {
        public string LedgerPage { get; set; }
        public string LedgerPageGUID { get; set; }
        
        public string ledger_name { get; set; }
        public string Ledger_code { get; set; }

        public string OHSNo { get; set; }
        public string ISGNo { get; set; }
        public string SSGNo { get; set; }
        public string PartNo { get; set; }
        public string Nomen { get; set; }
        public string AU { get; set; }
        public string NoOff { get; set; }
        public string SclAuth { get; set; }
        public string UnsvStock { get; set; }
        public string RepStock { get; set; }
        public string ServStock { get; set; }
        public string MSC { get; set; }
        public string Group { get; set; }
        public string CDS { get; set; }
        public string LPP { get; set; }
        public string Remarks { get; set; }
        public string Store { get; set; }
        public string SubStore { get; set; }
    }

}
