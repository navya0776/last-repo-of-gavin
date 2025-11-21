using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.ObjectModel;
using IMS.Models;



namespace IMS.ViewModels
{
    class Class1
    {
        public class FloorSummaryViewModel
{
    public ObservableCollection<Analysis> Rows { get; set; }

    public FloorSummaryViewModel()
    {
        Rows = new ObservableCollection<Analysis>()
        {
            new Analysis { Category="No of items", Total=1947, SerStk=673, PercentStk=34.5, TotStk=673, PercentTotStk=34.5, ZeroStock=1274, StockLT2=815, StockLT5=908, StockLT10=990 },
            new Analysis { Category="Scaled Items", Total=999, SerStk=567, PercentStk=56.7, TotStk=567, PercentTotStk=56.7, ZeroStock=432, StockLT2=432, StockLT5=508, StockLT10=578 },
            new Analysis { Category="Non Scaled Items", Total=948, RepStk=2, SerStk=106, PercentStk=11.1, TotStk=106, PercentTotStk=11.1, ZeroStock=842, StockLT2=383, StockLT5=400, StockLT10=412 },
            new Analysis { Category="Vital", Total=300, SerStk=250, PercentStk=83.3, TotStk=250, PercentTotStk=83.3, ZeroStock=50, StockLT2=20, StockLT5=30, StockLT10=45 },
            new Analysis { Category="Essential", Total=500, SerStk=350, PercentStk=70.0, TotStk=350, PercentTotStk=70.0, ZeroStock=150, StockLT2=80, StockLT5=110, StockLT10=130 },
            new Analysis { Category="Desirable", Total=450, SerStk=73, PercentStk=16.2, TotStk=73, PercentTotStk=16.2, ZeroStock=377, StockLT2=140, StockLT5=170, StockLT10=200 },
            new Analysis { Category="Must Change", Total=220, SerStk=180, PercentStk=81.8, TotStk=180, PercentTotStk=81.8, ZeroStock=40, StockLT2=18, StockLT5=25, StockLT10=35 },
            new Analysis { Category="Should Change", Total=310, SerStk=145, PercentStk=46.7, TotStk=145, PercentTotStk=46.7, ZeroStock=165, StockLT2=70, StockLT5=95, StockLT10=115 },
            new Analysis { Category="Could Change", Total=240, SerStk=35, PercentStk=14.6, TotStk=35, PercentTotStk=14.6, ZeroStock=205, StockLT2=80, StockLT5=90, StockLT10=110 },
            new Analysis { Category="Floor Must Change", Total=150, SerStk=120, PercentStk=80.0, TotStk=120, PercentTotStk=80.0, ZeroStock=30, StockLT2=15, StockLT5=22, StockLT10=28 },
            new Analysis { Category="Floor Should Change", Total=200, SerStk=92, PercentStk=46.0, TotStk=92, PercentTotStk=46.0, ZeroStock=108, StockLT2=60, StockLT5=70, StockLT10=82 },
            new Analysis { Category="Floor Could Change", Total=180, SerStk=18, PercentStk=10.0, TotStk=18, PercentTotStk=10.0, ZeroStock=162, StockLT2=55, StockLT5=65, StockLT10=72 },

        };
    }
}
    }
}
