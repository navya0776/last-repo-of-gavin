using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Models
{
    class Analysis
    {
        
            public string Category { get; set; }
            public int Total { get; set; }
            public int UnsvStk { get; set; }
            public int RepStk { get; set; }
            public int SerStk { get; set; }
            public double PercentStk { get; set; }
            public int D_In { get; set; }
            public int TotStk { get; set; }
            public double PercentTotStk { get; set; }
            public int ReOrdLevel { get; set; }
            public int SafetyStock { get; set; }
            public int ZeroStock { get; set; }
            public int StockLT2 { get; set; }
            public int StockLT5 { get; set; }
            public int StockLT10 { get; set; }
        

    }
}
