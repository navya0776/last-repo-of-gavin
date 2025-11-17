using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace SAPEAA.ViewModels
{
    public class ViewModel : INotifyPropertyChanged
    {
        public ObservableCollection<string> AvailableRoles { get; } = new()
        {
            "MT", "ENGR", "ORD", "ACSF", "INDG ARMY", "INDA INDG/VEH", "INDE"
        };

        private string _selectedRole;
        public string SelectedRole
        {
            get => _selectedRole;
            set
            {
                if (_selectedRole == value) return;
                _selectedRole = value;
                OnPropertyChanged();
                // Persist globally
                SAPEAA.Services.RoleManager.SetRole(_selectedRole);
            }
        }

        private DateTime _fromDate = new DateTime(2025, 4, 1);
        private DateTime _toDate = new DateTime(2026, 3, 31);

        public DateTime FromDate
        {
            get => _fromDate;
            set { _fromDate = value; OnPropertyChanged(); }
        }

        public DateTime ToDate
        {
            get => _toDate;
            set { _toDate = value; OnPropertyChanged(); }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string prop = null)
            => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
    }

    
}
