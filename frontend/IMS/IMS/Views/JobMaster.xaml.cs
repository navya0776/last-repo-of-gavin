using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace IMS.Views
{
    /// <summary>
    /// Interaction logic for JobMaster.xaml
    /// </summary>
    public partial class JobMaster : Page
    {
        private string _eqptCode;

        public ObservableCollection<JobMasterItem> JobList { get; set; }

        public JobMaster(string eqptCode)
        {
            InitializeComponent();

            _eqptCode = eqptCode;
            JobList = new ObservableCollection<JobMasterItem>();
            DataContext = this;

            LoadJobs();
        }

        private async void LoadJobs()
        {
            try
            {
                var list = await ApiService.GetJobsAsync(_eqptCode);
                JobList.Clear();

                foreach (var item in list)
                    JobList.Add(item);

                // Populate left active equipment panel
                ActiveEquipmentList.Items.Clear();
                ActiveEquipmentList.Items.Add(_eqptCode);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load job-master data.\n" + ex.Message,
                                "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

    }

}
