using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Models
{
    public class BasePermissions
    {
        public bool read { get; set; }
        public bool write { get; set; }
    }

    // Represents the full permissions object matching FastAPI's "Permissions" model
    public class Permissions
    {
        public BasePermissions ledger { get; set; }
        public BasePermissions apd { get; set; }
        public BasePermissions recieve_voucher { get; set; }
        public BasePermissions issue_voucher { get; set; }
        public BasePermissions local_purchase_indent { get; set; }
        public BasePermissions local_purchase_quotation { get; set; }
        public BasePermissions local_purchase_recieved { get; set; }
        public BasePermissions local_purchase_ordinance { get; set; }
        public BasePermissions local_purchase_pay { get; set; }
        public BasePermissions local_purchase_query { get; set; }
        public BasePermissions local_purchase_ammend { get; set; }
        public BasePermissions cds { get; set; }
    }

    // Represents a full user creation payload
    public class UserCreateRequest
    {
        public string username { get; set; }
        public string password { get; set; }
        public string role { get; set; }
        public Permissions permissions { get; set; }
    }

    // Optional: Represents a user returned from backend
    public class UserResponse
    {
        public string username { get; set; }
        public string role { get; set; }
        public Permissions permissions { get; set; }
        public bool new_user { get; set; }
    }
}
