using IMS.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Windows;
using static IMS.Windows.LoginWindow;

namespace IMS.Services
{
    public static class ApiService
    {
        // SINGLE shared HttpClient instance
        private static readonly CookieContainer CookieJar = new CookieContainer();
        private static readonly HttpClientHandler Handler;
        private static readonly HttpClient Client;

        static ApiService()
        {
            Handler = new HttpClientHandler()
            {
                UseCookies = true,
                CookieContainer = CookieJar,
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            Client = new HttpClient(Handler)
            {
                BaseAddress = new Uri("http://localhost:8000/")
            };

            Client.DefaultRequestHeaders.Accept.Clear();
            Client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }

        // -----------------------------------------------------
        // Cookie Debug
        // -----------------------------------------------------
        public static void PrintCookies()
        {
            var cookies = CookieJar.GetCookies(new Uri("http://localhost:8000/"));
            Console.WriteLine("\n--- Cookies ---");
            foreach (Cookie c in cookies)
                Console.WriteLine($"🍪 {c.Name} = {c.Value}");
            Console.WriteLine("----------------\n");
        }

        // -----------------------------------------------------
        // LOGIN
        // -----------------------------------------------------
        public static async Task<LoginResponse?> LoginAsync(string username, string password)
        {
            var payload = new { username, password };

            var response = await Client.PostAsJsonAsync("auth/login", payload);
            Console.WriteLine($"➡️ POST login -> {response.StatusCode}");

            if (!response.IsSuccessStatusCode)
            {
                string err = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"❌ Login failed: {err}");
                return null;
            }

            PrintCookies();
            return await response.Content.ReadFromJsonAsync<LoginResponse>();
        }

        // -----------------------------------------------------
        // LOGOUT
        // -----------------------------------------------------
        public static async Task<bool> LogoutAsync()
        {
            var resp = await Client.PostAsync("auth/logout", null);
            if (resp.IsSuccessStatusCode)
            {
                ClearSessionCookie();
                return true;
            }
            return false;
        }

        public static void ClearSessionCookie()
        {
            var uri = new Uri("http://localhost:8000/");
            var cookies = CookieJar.GetCookies(uri);

            foreach (Cookie cookie in cookies)
                cookie.Expired = true;
        }

        // -----------------------------------------------------
        // GENERIC HELPERS
        // -----------------------------------------------------
        public static async Task<T?> GetAsync<T>(string endpoint)
        {
            try
            {
                var resp = await Client.GetAsync(endpoint);
                Console.WriteLine($"➡️ GET {endpoint} -> {resp.StatusCode}");

                if (!resp.IsSuccessStatusCode)
                    return default;

                return await resp.Content.ReadFromJsonAsync<T>();
            }
            catch
            {
                return default;
            }
        }

        public static async Task<T?> PostAsync<T>(string endpoint, object body)
        {
            try
            {
                var resp = await Client.PostAsJsonAsync(endpoint, body);
                Console.WriteLine($"➡️ POST {endpoint} -> {resp.StatusCode}");

                if (!resp.IsSuccessStatusCode)
                    return default;

                return await resp.Content.ReadFromJsonAsync<T>();
            }
            catch
            {
                return default;
            }
        }

        public static async Task<bool> PostAsync(string endpoint, object body)
        {
            var resp = await Client.PostAsJsonAsync(endpoint, body);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<bool> DeleteAsync(string endpoint)
        {
            try
            {
                var resp = await Client.DeleteAsync(endpoint);

                if (!resp.IsSuccessStatusCode)
                {
                    string error = await resp.Content.ReadAsStringAsync();
                    MessageBox.Show($"error: {resp.StatusCode}\n\n{error}");
                    return false;
                }

                return true;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Exception: {ex.Message}");
                return false;
            }
        }

        // -----------------------------------------------------
        // FORGET PASSWORD
        // -----------------------------------------------------
        public static async Task<bool> ForgetPasswordAsync(string username, string newPassword)
        {
            var payload = new
            {
                username = username,
                new_user = true,
                new_password = newPassword
            };

            var resp = await Client.PostAsJsonAsync("auth/forget-password", payload);
            return resp.IsSuccessStatusCode;
        }

        // -----------------------------------------------------
        // LEDGER / STORES
        // -----------------------------------------------------
        public static async Task<List<(string store, List<string> substores)>> GetStoresAsync()
        {
            var resp = await Client.GetAsync("ledger/");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            var raw = JsonConvert.DeserializeObject<List<dynamic>>(json);

            var result = new List<(string store, List<string> subs)>();

            foreach (var r in raw)
            {
                string store = r.store_name ?? "";
                List<string> subs = new();

                try
                {
                    foreach (var s in r.ledgers)
                        subs.Add((string)s.Ledger_name);
                }
                catch { }

                result.Add((store, subs));
            }

            return result;
        }

        public static async Task<List<LedgerItem>> GetLedgerAsync(string ledger_code)
        {
            var resp = await Client.GetAsync($"ledger/?ledger_code={ledger_code}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<LedgerItem>>() ?? new();
        }

        public static async Task<LedgerItem?> CreateLedgerAsync(LedgerItem item)
        {
            var resp = await Client.PostAsJsonAsync($"ledger/?ledger_code={item.Ledger_code}", item);
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        public static async Task<bool> UpdateLedgerAsync(LedgerItem item)
        {
            try
            {
                var resp = await Client.PutAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);

                if (!resp.IsSuccessStatusCode)
                {
                    string error = await resp.Content.ReadAsStringAsync();
                    MessageBox.Show($"❌ 422 Validation Error:\n\n{error}", "Backend Error");
                    return false;
                }

                return true;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"❌ Update failed: {ex.Message}");
                return false;
            }
        }


        // -----------------------------------------------------
        // MASTER LIST
        // -----------------------------------------------------
        public static async Task<List<MasterListItem>> GetMasterListAsync()
        {
            var resp = await Client.GetAsync("cds/master-list");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<MasterListItem>>(json)
                   ?? new List<MasterListItem>();
        }

        // -----------------------------------------------------
        // EQUIPMENTS
        // -----------------------------------------------------
        public static async Task<bool> AddEquipmentAsync(AddEquipmentPayload payload)
        {
            var resp = await Client.PostAsJsonAsync("cds/", payload);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<List<EquipmentResponse>> GetAllEquipmentsAsync()
        {
            var resp = await Client.GetAsync("demand/equipments/");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<EquipmentResponse>>()
                   ?? new List<EquipmentResponse>();
        }

        // -----------------------------------------------------
        // JOB MASTER
        // -----------------------------------------------------
        public static async Task<List<JobMasterItem>> GetJobMasterAsync(string eqptCode)
        {
            var resp = await Client.GetAsync($"cds/job-master/{eqptCode}");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<JobMasterItem>>(json)
                   ?? new List<JobMasterItem>();
        }

        public static async Task<bool> AddJobMasterAsync(JobMasterPayload payload)
        {
            var resp = await Client.PostAsJsonAsync("cds/job-master", payload);
            return resp.IsSuccessStatusCode;
        }

        // -----------------------------------------------------
        // DEMAND
        // -----------------------------------------------------
        public static async Task<bool> CreateDemandAsync(DemandCreate payload)
        {
            var resp = await Client.PostAsJsonAsync("demand/", payload);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<List<DemandResponse>> GetAllDemandsAsync()
        {
            var resp = await Client.GetAsync("demand/");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
                   ?? new List<DemandResponse>();
        }

        public static async Task<List<DemandResponse>> GetDemandByNoAsync(int demandNo)
        {
            var resp = await Client.GetAsync($"demand/{demandNo}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
                   ?? new List<DemandResponse>();
        }

        public static async Task<bool> DeleteDemandAsync(int demandNo)
        {
            var resp = await Client.DeleteAsync($"demand/{demandNo}");
            return resp.IsSuccessStatusCode;
        }

        public static async Task<bool> LockDemandAsync(int demandNo)
        {
            var resp = await Client.PostAsync($"demand/{demandNo}/lock", null);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<bool> UnlockDemandAsync(int demandNo)
        {
            var resp = await Client.PostAsync($"demand/{demandNo}/unlock", null);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<List<DmdJunctionCreate>> GetDemandDetailsAsync(int demandNo)
        {
            var resp = await Client.GetAsync($"demand/detail/{demandNo}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DmdJunctionCreate>>()
                   ?? new List<DmdJunctionCreate>();
        }
    }
}





//using IMS.Models;
//using IMS.SAPEAAviews;
//using Newtonsoft.Json;
//using System;
//using System.Collections.Generic;
//using System.Diagnostics;
//using System.Net;
//using System.Net.Http;
//using System.Net.Http.Headers;
//using System.Net.Http.Json;
//using System.Text;
//using System.Threading.Tasks;
//using System.Windows;
//using static IMS.Windows.LoginWindow;

//namespace IMS.Services
//{
//    public static class ApiService
//    {
//        private static readonly CookieContainer _cookies = new CookieContainer();
//        private static readonly HttpClient _client;
//        private static HttpClientHandler _handler;


//        static ApiService()
//        {
//            _handler = new HttpClientHandler()
//            {
//                UseCookies = true,
//                CookieContainer = _cookies,
//                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
//            };

//            _client = new HttpClient(_handler)
//            {
//                BaseAddress = new Uri("http://localhost:8000/")
//            };

//            _client.DefaultRequestHeaders.Accept.Clear();
//            _client.DefaultRequestHeaders.Accept.Add(
//                new MediaTypeWithQualityHeaderValue("application/json"));
//        }
//        public static void PrintCookies()
//        {
//            var cookies = _handler.CookieContainer.GetCookies(new Uri("http://localhost:8000/"));

//            Console.WriteLine("\n--- STORED COOKIES ---");
//            foreach (Cookie cookie in cookies)
//            {
//                Console.WriteLine($"🍪 {cookie.Name} = {cookie.Value}");
//            }
//            Console.WriteLine("----------------------\n");
//        }


//        // ------------------------------
//        // LOGIN
//        public static async Task<bool> LoginAsync(string username, string password)
//        {
//            var payload = new { username, password };
//            var response = await _client.PostAsJsonAsync("auth/login", payload);
//            if (!response.IsSuccessStatusCode)
//            {
//                Console.WriteLine("❌ Login failed");
//                return false;
//            }

//            PrintCookies();

//            Debug.WriteLine("✅ Login succeeded");
//            //        var cookies = ((HttpClientHandler)_handler).CookieContainer
//            //.GetCookies(new Uri("http://localhost:8000/"));

//            //        foreach (Cookie cookie in cookies)
//            //            Console.WriteLine($"🍪 Cookie stored: {cookie.Name} = {cookie.Value}");


//            // HttpClientHandler is already storing cookies automatically
//            return true;
//        }


//        // ------------------------------
//        // COOKIE SET
//        //public static void SetAuthCookie(string name, string value, string domain)
//        //{
//        //    _cookies.Add(new Cookie(name, value) { Domain = domain });
//        //}

//        // ------------------------------
//        // STORES
//        public static async Task<List<(string store, List<string> substores)>> GetStoresAsync()
//        {
//            var resp = await _client.GetAsync("ledger/");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            var raw = JsonConvert.DeserializeObject<List<dynamic>>(json);

//            var result = new List<(string store, List<string> subs)>();
//            foreach (var r in raw)
//            {
//                // Match backend keys
//                string store = r.store_name ?? "";
//                List<string> subs = new();

//                try
//                {
//                    foreach (var s in r.ledgers)
//                    {
//                        subs.Add((string)s.Ledger_name); // from your backend response
//                    }
//                }
//                catch { }

//                result.Add((store, subs));
//            }

//            return result;
//        }


//        // ------------------------------
//        // LEDGER GET (equipment pages)
//        // ------------------------------
//        public static async Task<List<LedgerItem>> GetLedgerAsync(string ledger_code)
//        {
//            var resp = await _client.GetAsync($"/ledger/?ledger_code={ledger_code}");
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<List<LedgerItem>>() ?? new();
//        }

//        // ------------------------------
//        // LEDGER CREATE
//        // ------------------------------
//        public static async Task<LedgerItem?> CreateLedgerAsync(LedgerItem item)
//        {
//            var resp = await _client.PostAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
//            resp.EnsureSuccessStatusCode();
//            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
//        }

//        // ------------------------------
//        // LEDGER UPDATE
//        // ------------------------------
//        public static async Task<LedgerItem?> UpdateLedgerAsync(string pageName, LedgerItem item)
//        {
//            var resp = await _client.PutAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
//            resp.EnsureSuccessStatusCode();
//            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
//        }

//        //// ------------------------------
//        //// ADD PAGE TO EQUIPMENT
//        //// ------------------------------
//        //public static async Task<bool> AddPageAsync(string equipment, LedgerItem page)
//        //{
//        //    var resp = await _client.PostAsJsonAsync($"/", page);
//        //    resp.EnsureSuccessStatusCode();
//        //    return true;
//        //}

//        // ------------------------------
//        // GENERIC GET
//        // ------------------------------
//        public static async Task<T?> GetAsync<T>(string endpoint)
//        {
//            var resp = await _client.GetAsync(endpoint);
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<T>();
//        }

//        // ------------------------------
//        // GENERIC POST
//        // ------------------------------
//        public static async Task<T?> PostAsync<T>(string endpoint, object body)
//        {
//            var resp = await _client.PostAsJsonAsync(endpoint, body);
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<T>();
//        }

//        // ------------------------------
//        // GENERIC DELETE
//        // ------------------------------
//        public static async Task DeleteAsync(string endpoint)
//        {
//            try
//            {
//                var resp = await _client.DeleteAsync(endpoint);
//                if (!resp.IsSuccessStatusCode)
//                {
//                    string error = await resp.Content.ReadAsStringAsync();
//                    MessageBox.Show($"error: {resp.StatusCode}\n\n{error}");
//                    return;
//                }
//            }
//            catch(Exception ex)
//            {
//                MessageBox.Show($"Exception: {ex.Message}");
//            }
//        }

//        // ------------------------------
//        // GET CDS LIST (Central Demand)
//        // ------------------------------
//        public static async Task<List<CDS>> GetCDSAsync()
//        {
//            var resp = await _client.GetAsync("cds/");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            return JsonConvert.DeserializeObject<List<CDS>>(json) ?? new List<CDS>();
//        }

//        public static async Task<List<MasterListItem>> GetMasterListAsync()
//        {
//            var resp = await _client.GetAsync("cds/master-list");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            return JsonConvert.DeserializeObject<List<MasterListItem>>(json)
//                   ?? new List<MasterListItem>();
//        }

//        public static async Task<bool> AddEquipmentAsync(AddEquipmentPayload payload)
//        {
//            var resp = await _client.PostAsJsonAsync("cds/", payload);

//            if (!resp.IsSuccessStatusCode)
//                return false;

//            return true;
//        }
//        public static async Task<List<JobMasterItem>> GetJobMasterAsync(string eqptCode)
//        {
//            var resp = await _client.GetAsync($"cds/job-master/{eqptCode}");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            return JsonConvert.DeserializeObject<List<JobMasterItem>>(json)
//                   ?? new List<JobMasterItem>();
//        }

//        public static async Task<bool> AddJobMasterAsync(JobMasterPayload payload)
//        {
//            var resp = await _client.PostAsJsonAsync("cds/job-master", payload);

//            if (!resp.IsSuccessStatusCode)
//                return false;

//            return true;
//        }
//        public static async Task<List<JobMasterItem>> GetJobsAsync(string eqptCode)
//        {
//            var resp = await _client.GetAsync($"cds/job-master/{eqptCode}");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            return JsonConvert.DeserializeObject<List<JobMasterItem>>(json)
//                   ?? new List<JobMasterItem>();
//        }

//        public static async Task<List<LPRItem>> GetLPRListAsync()
//        {
//            var resp = await _client.GetAsync("lpr/");
//            resp.EnsureSuccessStatusCode();

//            var json = await resp.Content.ReadAsStringAsync();
//            return JsonConvert.DeserializeObject<List<LPRItem>>(json)
//                   ?? new List<LPRItem>();
//        }

//        public static async Task<bool> ForgetPasswordAsync(string username, string newPassword)
//        {
//            var payload = new
//            {
//                username = username,
//                new_user = true,   // REQUIRED BY BACKEND
//                new_password = newPassword
//            };

//            var response = await ApiClient.PostAsync<Dictionary<string, string>>(
//                "auth/forget-password",
//                payload
//            );

//            return response != null;
//        }

//        public static void ClearSessionCookie()
//        {
//            var uri = new Uri("http://localhost:8000/");
//            var cookies = _handler.CookieContainer.GetCookies(uri);

//            foreach (Cookie cookie in cookies)
//            {
//                if (cookie.Name == "session_id")
//                {
//                    cookie.Expired = true;
//                }
//            }
//        }


//        public static async Task<bool> LogoutAsync()
//        {
//            var response = await _client.PostAsync("auth/logout", new StringContent(""));

//            if (response.IsSuccessStatusCode)
//            {
//                ClearSessionCookie();   // 🔥 Force remove locally
//                return true;
//            }

//            return false;
//        }



//        public static async Task<bool> CreateDemandAsync(DemandCreate payload)
//        {
//            var resp = await _client.PostAsJsonAsync("demand/", payload);
//            return resp.IsSuccessStatusCode;
//        }

//        public static async Task<List<DemandResponse>> GetAllDemandsAsync()
//        {
//            var resp = await _client.GetAsync("demand/");
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
//                   ?? new List<DemandResponse>();
//        }

//        public static async Task<List<DemandResponse>> GetDemandByNoAsync(int demandNo)
//        {
//            var resp = await _client.GetAsync($"demand/{demandNo}");
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
//                   ?? new List<DemandResponse>();
//        }
//        public static async Task<bool> DeleteDemandAsync(int demandNo)
//        {
//            var resp = await _client.DeleteAsync($"demand/{demandNo}");
//            return resp.IsSuccessStatusCode;
//        }
//        public static async Task<bool> LockDemandAsync(int demandNo)
//        {
//            var resp = await _client.PostAsync($"demand/{demandNo}/lock", null);
//            return resp.IsSuccessStatusCode;
//        }
//        public static async Task<bool> UnlockDemandAsync(int demandNo)
//        {
//            var resp = await _client.PostAsync($"demand/{demandNo}/unlock", null);
//            return resp.IsSuccessStatusCode;
//        }
//        public static async Task<List<DmdJunctionCreate>> GetDemandDetailsAsync(int demandNo)
//        {
//            var resp = await _client.GetAsync($"demand/detail/{demandNo}");
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<List<DmdJunctionCreate>>()
//                   ?? new List<DmdJunctionCreate>();
//        }
//        public static async Task<List<EquipmentResponse>> GetAllEquipmentsAsync()
//        {
//            var resp = await _client.GetAsync("demand/equipments/");
//            resp.EnsureSuccessStatusCode();

//            return await resp.Content.ReadFromJsonAsync<List<EquipmentResponse>>()
//                   ?? new List<EquipmentResponse>();
//        }


//    }
//}
