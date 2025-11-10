using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Models
{
        public class CDS
        {
            public bool SEL { get; set; }

            public string LedgPage { get; set; }
            public string OHSNo { get; set; }
            public string PartNo { get; set; }
            public string Spart_No { get; set; }
            public string Nomen { get; set; }
            public string AU { get; set; }
            public string NoOff { get; set; }
            public string OHSAuth { get; set; }

            public string Dem { get; set; }
            public string AddlDem { get; set; }

            public string OSSIss { get; set; }
            public string CDSIss { get; set; }
            public string CDSStk { get; set; }

            public string JobNo { get; set; }
            public DateTime? JobDate { get; set; }

            public string DemNo { get; set; }
            public DateTime? DemDt { get; set; }

            public string AddiDno { get; set; }
            public DateTime? AddiDemdt { get; set; }

            public bool LPR { get; set; }
            public string LPRQty { get; set; }
            public string LPRNo { get; set; }
            public DateTime? LPRdt { get; set; }

            public string DemandCtrlNo { get; set; }
            public DateTime? DemandCtrlDate { get; set; }

            public string CurrStk { get; set; }
            public string NowIssue { get; set; }

            public string RecdQty { get; set; }
            public DateTime? DateNR { get; set; }

            public string Qty1 { get; set; }
            public string OSSIV1 { get; set; }
            public DateTime? OSSIV_dt1 { get; set; }

            public string Qty2 { get; set; }
            public string OSSIV2 { get; set; }
            public DateTime? OSSIV_dt2 { get; set; }

            public string Qty3 { get; set; }
            public string OSSIV3 { get; set; }
            public DateTime? OSSIV_dt3 { get; set; }

            public string CDSqt1 { get; set; }
            public string CDSIV1 { get; set; }
            public DateTime? CDSIV_dt1 { get; set; }

            public string CDSqt2 { get; set; }
            public string CDSIV2 { get; set; }
            public DateTime? CDSIV_dt2 { get; set; }

            public string CDSqt3 { get; set; }
            public string CDSIV3 { get; set; }
            public DateTime? CDSIV_dt3 { get; set; }

            public string DemID { get; set; }
        }
    }

