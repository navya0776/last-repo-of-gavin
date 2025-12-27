using IMS.Models;
using IMS.Services;
using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class CentralDemandNavigationPage : Page
    {
        // LEFT SIDE LISTS
        public ObservableCollection<string> JobList { get; set; } = new();
        public ObservableCollection<string> DemList { get; set; } = new();
        public ObservableCollection<string> LPRList { get; set; } = new();

        // MAIN DATAGRID LIST
        public ObservableCollection<CDSRowMock> LedgerRows { get; set; } = new();

        private readonly string _eqptCode;

        public CentralDemandNavigationPage(string eqptCode)
        {
            InitializeComponent();
            _eqptCode = eqptCode;

            DataContext = this;

            LoadMockData();   // Using mock data for now
            // LoadCDS();     // <-- API integration preserved (commented for now)
        }

        /* ---------------------------------------------------------
           MOCK DATA (Used for now, until backend is ready)
        ----------------------------------------------------------*/
        private void LoadMockData()
        {
            try
            {
                // JOB LIST (LEFT PANEL)
                JobList.Clear();
                for (int i = 1; i <= 10; i++)
                    JobList.Add($"JOB-{1000 + i}   |   {DateTime.Now.AddDays(-i):dd-MM-yyyy}");

                // DEMAND LIST
                DemList.Clear();
                for (int i = 1; i <= 8; i++)
                    DemList.Add($"DEM-{2000 + i}   |   {DateTime.Now.AddDays(-i):dd-MM-yyyy}");

                // LPR LIST
                LPRList.Clear();
                for (int i = 1; i <= 6; i++)
                    LPRList.Add($"LPR-{3000 + i}");

                // LEDGER ROWS
                LedgerRows.Clear();
                Random R = new Random();

                for (int i = 1; i <= 50; i++)
                {
                    LedgerRows.Add(new CDSRowMock
                    {
                        SEL = false,
                        LedgPage = $"LP-{i}",
                        OHSNo = $"OHS-{200 + i}",
                        PartNo = $"PN-{i}",
                        Spart_No = $"SP-{i}",
                        Nomen = $"Part Description {i}",
                        AU = (i % 2 == 0) ? "EA" : "NOS",
                        NoOff = R.Next(1, 20),
                        OHSAuth = $"AUTH-{i}",
                        Dem = R.Next(0, 20),
                        AddlDem = R.Next(0, 10),
                        OSSIss = R.Next(0, 15),
                        CDSIss = R.Next(0, 10),
                        CDSStk = R.Next(5, 50),
                        JobNo = $"JOB-{1000 + (i % 10)}",
                        JobDate = DateTime.Now.AddDays(-i).ToString("dd-MM-yyyy"),
                        DemNo = $"DEM-{2000 + (i % 8)}",
                        DemDt = DateTime.Now.AddDays(-i - 2).ToString("dd-MM-yyyy"),
                        AddiDno = $"ADD-{i}",
                        AddiDemdt = DateTime.Now.AddDays(-i - 3).ToString("dd-MM-yyyy"),
                        LPR = (i % 3 == 0),
                        LPRQty = R.Next(0, 15),
                        LPRNo = $"LPR-{3000 + (i % 6)}",
                        LPRdt = DateTime.Now.AddDays(-i - 4).ToString("dd-MM-yyyy"),
                        DemandCtrlNo = $"CTRL-{i}",
                        DemandCtrlDate = DateTime.Now.AddDays(-i - 5).ToString("dd-MM-yyyy"),
                        CurrStk = R.Next(0, 40),
                        NowIssue = R.Next(0, 10),
                        RecdQty = R.Next(0, 20),
                        DateNR = DateTime.Now.AddDays(-i - 6).ToString("dd-MM-yyyy"),
                        Qty1 = R.Next(0, 10),
                        OSSIV1 = $"IV-{i}-1",
                        OSSIV_dt1 = DateTime.Now.AddDays(-i - 1).ToString("dd-MM-yyyy"),
                        Qty2 = R.Next(0, 10),
                        OSSIV2 = $"IV-{i}-2",
                        OSSIV_dt2 = DateTime.Now.AddDays(-i - 2).ToString("dd-MM-yyyy"),
                        Qty3 = R.Next(0, 10),
                        OSSIV3 = $"IV-{i}-3",
                        OSSIV_dt3 = DateTime.Now.AddDays(-i - 3).ToString("dd-MM-yyyy"),
                        CDSqt1 = R.Next(0, 10),
                        CDSIV1 = $"CIV-{i}-1",
                        CDSIV_dt1 = DateTime.Now.AddDays(-i - 4).ToString("dd-MM-yyyy"),
                        CDSqt2 = R.Next(0, 10),
                        CDSIV2 = $"CIV-{i}-2",
                        CDSIV_dt2 = DateTime.Now.AddDays(-i - 5).ToString("dd-MM-yyyy"),
                        CDSqt3 = R.Next(0, 10),
                        CDSIV3 = $"CIV-{i}-3",
                        CDSIV_dt3 = DateTime.Now.AddDays(-i - 6).ToString("dd-MM-yyyy"),
                        DemID = $"DID-{i}"
                    });
                }
            }
            catch (Exception ex)
            {
                //MessageBox.Show("Mock data creation error:\n" + ex.Message);
            }
        }

        /* ---------------------------------------------------------
           REAL BACKEND (API) — Preserved, commented for now
        ----------------------------------------------------------*/
        private async void LoadCDS()
        {
            try
            {
                /*
                var apiData = await ApiService.GetCDSAsync();

                var filtered = apiData.Where(x => x.eqpt_code == _eqptCode);

                LedgerRows.Clear();
                foreach (var item in filtered)
                {
                    LedgerRows.Add(new CDSRowMock
                    {
                        SEL = false,
                        LedgPage = item.ledg_page,
                        OHSNo = item.ohs_number,
                        PartNo = item.part_number,
                        Spart_No = item.spart_no,
                        Nomen = item.nomenclature,
                        AU = item.a_u,
                        NoOff = item.no_off,
                        OHSAuth = item.ohs_auth,
                        Dem = item.dem,
                        AddlDem = item.addl_dem,
                        OSSIss = item.oss_iss,
                        CDSIss = item.cds_iss,
                        CDSStk = item.cds_stk,
                        // etc... fill all fields
                    });
                }
                */
            }
            catch (Exception ex)
            {
                //MessageBox.Show("Failed to load CDS data.\n" + ex.Message);
            }
        }

        /* ---------------------------------------------------------
           CLOSE BUTTON
        ----------------------------------------------------------*/
        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.GoBack();
        }
    }


    /* ---------------------------------------------------------
       MOCK MODEL (Matches DataGrid Columns EXACTLY)
    ----------------------------------------------------------*/
    public class CDSRowMock
    {
        public bool SEL { get; set; }
        public string LedgPage { get; set; }
        public string OHSNo { get; set; }
        public string PartNo { get; set; }
        public string Spart_No { get; set; }
        public string Nomen { get; set; }
        public string AU { get; set; }
        public int NoOff { get; set; }
        public string OHSAuth { get; set; }
        public int Dem { get; set; }
        public int AddlDem { get; set; }
        public int OSSIss { get; set; }
        public int CDSIss { get; set; }
        public int CDSStk { get; set; }
        public string JobNo { get; set; }
        public string JobDate { get; set; }
        public string DemNo { get; set; }
        public string DemDt { get; set; }
        public string AddiDno { get; set; }
        public string AddiDemdt { get; set; }
        public bool LPR { get; set; }
        public int LPRQty { get; set; }
        public string LPRNo { get; set; }
        public string LPRdt { get; set; }
        public string DemandCtrlNo { get; set; }
        public string DemandCtrlDate { get; set; }
        public int CurrStk { get; set; }
        public int NowIssue { get; set; }
        public int RecdQty { get; set; }
        public string DateNR { get; set; }
        public int Qty1 { get; set; }
        public string OSSIV1 { get; set; }
        public string OSSIV_dt1 { get; set; }
        public int Qty2 { get; set; }
        public string OSSIV2 { get; set; }
        public string OSSIV_dt2 { get; set; }
        public int Qty3 { get; set; }
        public string OSSIV3 { get; set; }
        public string OSSIV_dt3 { get; set; }
        public int CDSqt1 { get; set; }
        public string CDSIV1 { get; set; }
        public string CDSIV_dt1 { get; set; }
        public int CDSqt2 { get; set; }
        public string CDSIV2 { get; set; }
        public string CDSIV_dt2 { get; set; }
        public int CDSqt3 { get; set; }
        public string CDSIV3 { get; set; }
        public string CDSIV_dt3 { get; set; }
        public string DemID { get; set; }
    }
}
