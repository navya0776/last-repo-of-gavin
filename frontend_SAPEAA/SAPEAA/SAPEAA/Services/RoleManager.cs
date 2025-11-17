using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SAPEAA.Services
{
    public static class RoleManager
    {
        private static string _currentRole;
        public static string CurrentRole => _currentRole;

        public static void SetRole(string role)
        {
            _currentRole = role;
            // optionally raise events / notify other parts of app
        }
    }

    
}
