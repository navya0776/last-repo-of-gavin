using DocumentFormat.OpenXml.Spreadsheet;
using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Views
{
    public partial class AdminDashboatd : System.Windows.Controls.Page
    {
        public AdminDashboatd()
        {
            InitializeComponent();
            LoadUsers();
        }

        private async void RefreshUsers_Click(object sender, RoutedEventArgs e)
        {
            await LoadUsers();
        }

        private async Task LoadUsers()
        {
            try
            {
                var users = await ApiService.GetAsync<List<UserResponse>>("admin/users/");

                if (users == null || users.Count == 0)
                {
                    MessageBox.Show("No users found.");
                    UsersList.ItemsSource = null;
                    return;
                }

                UsersList.ItemsSource = users;
                UsersList.DisplayMemberPath = "username"; 
                UsersList.SelectedValuePath = "username"; 

                //MessageBox.Show($"✅ Loaded {users.Count} users successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"❌ Error loading users: {ex.Message}");
            }
        }


        private void UsersList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (UsersList.SelectedItem is UserResponse selectedUser)
            {
                SelectedUsername.Text = selectedUser.username;
                SelectedRole.Text = selectedUser.role;
                //MessageBox.Show(JsonSerializer.Serialize(selectedUser.permissions));

                PermissionsPanel.Children.Clear();

                var perms = selectedUser.permissions;

                foreach (var prop in typeof(Permissions).GetProperties())
                {
                    var permValue = prop.GetValue(perms) as BasePermissions;

                    // FIX: if backend sent null → replace with {read = false, write = false}
                    if (permValue == null)
                        permValue = new BasePermissions { read = false, write = false };

                    PermissionsPanel.Children.Add(new TextBlock
                    {
                        Text = $"{prop.Name}: Read = {permValue.read}, Write = {permValue.write}",
                        Margin = new Thickness(2)
                    });
                }
            }
        }



        private Permissions BuildPermissions()
        {
            // Define all required permission keys as per backend
            string[] keys = new[]
            {
        "ledger",
        "apd",
        "recieve_voucher",
        "issue_voucher",
        "local_purchase_indent",
        "local_purchase_quotation",
        "local_purchase_recieved",
        "local_purchase_ordinance",
        "local_purchase_pay",
        "local_purchase_query",
        "local_purchase_ammend",
        "cds"
    };

            var permissions = new Permissions();

            // Initialize every permission to {read=false, write=false}
            foreach (var key in keys)
            {
                var prop = typeof(Permissions).GetProperty(key);
                if (prop != null)
                {
                    prop.SetValue(permissions, new BasePermissions { read = false, write = false });
                }
            }

            // Update based on actual checkboxes
            foreach (var key in keys)
            {
                // Look for checkboxes named like LedgerRead, LedgerWrite, etc.
                var readCheckbox = FindName($"{key.First().ToString().ToUpper() + key.Substring(1)}Read") as CheckBox;
                var writeCheckbox = FindName($"{key.First().ToString().ToUpper() + key.Substring(1)}Write") as CheckBox;


                var prop = typeof(Permissions).GetProperty(key);
                if (prop != null)
                {
                    prop.SetValue(permissions, new BasePermissions
                    {
                        read = readCheckbox?.IsChecked == true,
                        write = writeCheckbox?.IsChecked == true
                    });
                }
            }

            return permissions;
        }


        private async void SubmitNewUser_Click(object sender, RoutedEventArgs e)
        {
            var newUser = new UserCreateRequest
            {
                username = NewUsernameInput.Text.Trim(),
                password = NewPasswordInput.Password.Trim(),
                role = (RoleComboBox.SelectedItem as ComboBoxItem)?.Content.ToString(),
                permissions = BuildPermissions()
            };

            var result = await ApiService.PostAsync<object>("admin/user", newUser);
            MessageBox.Show(result != null ? "User created successfully!" : "Failed to create user.");
        }




        private async void DeleteUser_Click(object sender, RoutedEventArgs e)
        {
            if (UsersList.SelectedItem is not UserResponse selectedUser)
            {
                MessageBox.Show("Please select a user to delete.");
                return;
            }

            if (selectedUser.username == "admin")
            {
                MessageBox.Show("Admin user cannot be deleted!");
                return;
            }

            // Confirm deletion
            var result = MessageBox.Show(
                $"Are you sure you want to delete '{selectedUser.username}'?",
                "Confirm Delete",
                MessageBoxButton.YesNo,
                MessageBoxImage.Warning
            );

            if (result != MessageBoxResult.Yes)
                return;

            try
            {
                // API call to delete the user
                await ApiService.DeleteAsync($"admin/user/{selectedUser.username}");

                MessageBox.Show($"User '{selectedUser.username}' deleted successfully!");

                // Refresh UI
                await LoadUsers();

                SelectedUsername.Text = "";
                SelectedRole.Text = "";
                PermissionsPanel.Children.Clear();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to delete user: {ex.Message}");
               
            }
        }


        private void ViewAuditLogs_Click(object sender, RoutedEventArgs e)
        {
            // optional log viewer
        }


    }
}
