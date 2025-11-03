using IMS.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class AdminDashboatd : Page
    {

        public class PermissionItem
        {
            public bool read { get; set; }
            public bool write { get; set; }
        }

        public class UserDto
        {
            public string username { get; set; }
            public bool new_user { get; set; }
            public string role { get; set; }
            public Dictionary<string, PermissionItem> Permissions { get; set; }
        }

        public class AuditLogRequest
        {
            public string? username { get; set; } // null shows ALL
            public int start { get; set; }
            public int end { get; set; }
        }




        // Mock backend store
        private List<UserDto> _users = new();
        private UserDto _selectedUser;

        // Available permissions (system supported)
        private readonly string[] _allPermissions =
        {
            "View Ledger", "Edit Ledger", "Export",
            "Admin Access", "Manage Users", "View Audit Logs"
        };

        public AdminDashboatd()
        {
            InitializeComponent();
            PopulateUserList();
            Loaded += AdminDashboatd_Loaded;

        }
        private async void AdminDashboatd_Loaded(object sender, RoutedEventArgs e)
        {
            await LoadUsersAndLogs();
        }

        private async Task LoadUsersAndLogs()
        {
            try
            {
                _users = await ApiClient.PostAsync<List<UserDto>>("admin/users/", null)
                         ?? new List<UserDto>();

                UsersList.ItemsSource = _users.Select(u => u.username).ToList();

                // Load all audit logs by default
                var logs = await GetAuditLogs(null, 0, 50);
                AuditList.ItemsSource = logs ?? new List<AuditLogRequest>();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"LoadUsersAndLogs failed: {ex.Message}");
            }
        }


        // Mock data loader

        // Fill left list
        private async void PopulateUserList()
        {
            _users = await ApiClient.PostAsync<List<UserDto>>("admin/users/", null);

            if (_users == null)
            {
                MessageBox.Show("Failed to load users!");
                return;
            }

            UsersList.ItemsSource = _users.Select(u => u.username);
        }

        private async Task<List<AuditLogRequest>?> GetAuditLogs(string? username, int start, int end)
        {
            try
            {
                var req = new AuditLogRequest
                {
                    username = username,
                    start = start,
                    end = end
                };

                // endpoint path — update if different
                var logs = await ApiClient.PostAsync<List<AuditLogRequest>>("admin/audit_logs/", req);

                if (logs == null)
                {
                    MessageBox.Show("No audit logs returned (null).");
                }

                return logs;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"GetAuditLogs failed: {ex.Message}\n{ex.StackTrace}");
                return null;
            }
        }



        // When user is clicked
        private async void UsersList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (UsersList.SelectedItem == null)
            {
                var logs = await GetAuditLogs(null, 0, 50);
                AuditList.ItemsSource = logs;
                return;
            }

            string username = UsersList.SelectedItem.ToString();

            // Fetch user detail from backend 
            _selectedUser = await ApiClient.GetAsync<UserDto>($"admin/users/{username}/");



            if (_selectedUser == null)
            {
                MessageBox.Show("User details not found!");
                return;
            }

            SelectedUsername.Text = _selectedUser.username;
            SelectedRole.Text = _selectedUser.role;

            PopulatePermissionCheckboxes();
            var userLogs = await GetAuditLogs(_selectedUser.username, 0, 50);
            AuditList.ItemsSource = userLogs;

        }



        // Dynamically generate permission checkboxes
        private void PopulatePermissionCheckboxes()
        {
            PermissionsPanel.Children.Clear();

            if (_selectedUser?.Permissions == null) return;

            foreach (var kv in _selectedUser.Permissions)
            {
                var stack = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 4, 0, 4) };

                stack.Children.Add(new TextBlock
                {
                    Text = kv.Key,
                    Width = 160,
                    VerticalAlignment = VerticalAlignment.Center
                });

                stack.Children.Add(new CheckBox
                {
                    Content = "Read",
                    IsChecked = kv.Value.read,
                    IsEnabled = false,
                    VerticalAlignment = VerticalAlignment.Center
                });

                stack.Children.Add(new CheckBox
                {
                    Content = "Write",
                    IsChecked = kv.Value.write,
                    IsEnabled = false,
                    Margin = new Thickness(8, 0, 0, 0),
                    VerticalAlignment = VerticalAlignment.Center
                });

                PermissionsPanel.Children.Add(stack);
            }
        }


        // On checking/unchecking permissions


        // Save button click


        // Audit logs popup mock
        private void ViewAuditLogs_Click(object sender, RoutedEventArgs e)
        {
            /*
             * Send me JSON
             * {
             *   username: string | None, string for a specific user, None for all users
             *   start: int, start from today's number of audit logs - x 
             *   end: self explanatory
             *   }
             */
            /*
             * Same as above
             */

            MessageBox.Show("Audit Logs:\n- Admin modified user permissions\n- StoreA_user exported Ledger");
        }
    }

}
