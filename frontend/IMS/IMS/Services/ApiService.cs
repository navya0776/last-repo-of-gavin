using IMS.Models;
using IMS.SAPEAAviews;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using static IMS.Windows.LoginWindow;

namespace IMS.Services
{
    public static class ApiService
    {
        private static readonly CookieContainer _cookies = new CookieContainer();
        private static readonly HttpClient _client;
        private static HttpClientHandler _handler;


        static ApiService()
        {
            _handler = new HttpClientHandler()
            {
                UseCookies = true,
                CookieContainer = _cookies,
                AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate,
            };

            _client = new HttpClient(_handler)
            {
                BaseAddress = new Uri("http://localhost:8000/")
            };

            _client.DefaultRequestHeaders.Accept.Clear();
            _client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
        }
        public static void PrintCookies()
        {
            var cookies = _handler.CookieContainer.GetCookies(new Uri("http://localhost:8000/"));
            foreach (Cookie cookie in cookies)
            {
                Console.WriteLine($"🍪 {cookie.Name} = {cookie.Value}");
            }
        }

        // ------------------------------
        // LOGIN
        public static async Task<bool> LoginAsync(string username, string password)
        {
            var payload = new { username, password };
            var response = await _client.PostAsJsonAsync("auth/login", payload);
            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine("❌ Login failed");
                return false;
            }

            PrintCookies();

            Debug.WriteLine("✅ Login succeeded");
            //        var cookies = ((HttpClientHandler)_handler).CookieContainer
            //.GetCookies(new Uri("http://localhost:8000/"));

            //        foreach (Cookie cookie in cookies)
            //            Console.WriteLine($"🍪 Cookie stored: {cookie.Name} = {cookie.Value}");


            // HttpClientHandler is already storing cookies automatically
            return true;
        }


        // ------------------------------
        // COOKIE SET
        //public static void SetAuthCookie(string name, string value, string domain)
        //{
        //    _cookies.Add(new Cookie(name, value) { Domain = domain });
        //}

        // ------------------------------
        // STORES
        public static async Task<List<(string store, List<string> substores)>> GetStoresAsync()
        {
            var resp = await _client.GetAsync("ledger/");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            var raw = JsonConvert.DeserializeObject<List<dynamic>>(json);

            var result = new List<(string store, List<string> subs)>();
            foreach (var r in raw)
            {
                // Match backend keys
                string store = r.store_name ?? "";
                List<string> subs = new();

                try
                {
                    foreach (var s in r.ledgers)
                    {
                        subs.Add((string)s.Ledger_name); // from your backend response
                    }
                }
                catch { }

                result.Add((store, subs));
            }

            return result;
        }


        // ------------------------------
        // LEDGER GET (equipment pages)
        // ------------------------------
        public static async Task<List<LedgerItem>> GetLedgerAsync(string ledger_code)
        {
            var resp = await _client.GetAsync($"/ledger/?ledger_code={ledger_code}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<LedgerItem>>() ?? new();
        }

        // ------------------------------
        // LEDGER CREATE
        // ------------------------------
        public static async Task<LedgerItem?> CreateLedgerAsync(LedgerItem item)
        {
            var resp = await _client.PostAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        // ------------------------------
        // LEDGER UPDATE
        // ------------------------------
        public static async Task<LedgerItem?> UpdateLedgerAsync(string pageName, LedgerItem item)
        {
            var resp = await _client.PutAsJsonAsync($"/ledger/?ledger_code={item.Ledger_code}", item);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<LedgerItem>();
        }

        //// ------------------------------
        //// ADD PAGE TO EQUIPMENT
        //// ------------------------------
        //public static async Task<bool> AddPageAsync(string equipment, LedgerItem page)
        //{
        //    var resp = await _client.PostAsJsonAsync($"/", page);
        //    resp.EnsureSuccessStatusCode();
        //    return true;
        //}

        // ------------------------------
        // GENERIC GET
        // ------------------------------
        public static async Task<T?> GetAsync<T>(string endpoint)
        {
            var resp = await _client.GetAsync(endpoint);
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<T>();
        }

        // ------------------------------
        // GENERIC POST
        // ------------------------------
        public static async Task<T?> PostAsync<T>(string endpoint, object body)
        {
            var resp = await _client.PostAsJsonAsync(endpoint, body);
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<T>();
        }

        // ------------------------------
        // GENERIC DELETE
        // ------------------------------
        public static async Task DeleteAsync(string endpoint)
        {
            var resp = await _client.DeleteAsync(endpoint);
            resp.EnsureSuccessStatusCode();
        }

        // ------------------------------
        // GET CDS LIST (Central Demand)
        // ------------------------------
        public static async Task<List<CDS>> GetCDSAsync()
        {
            var resp = await _client.GetAsync("cds/");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<CDS>>(json) ?? new List<CDS>();
        }

        public static async Task<List<MasterListItem>> GetMasterListAsync()
        {
            var resp = await _client.GetAsync("cds/master-list");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<MasterListItem>>(json)
                   ?? new List<MasterListItem>();
        }

        public static async Task<bool> AddEquipmentAsync(AddEquipmentPayload payload)
        {
            var resp = await _client.PostAsJsonAsync("cds/", payload);

            if (!resp.IsSuccessStatusCode)
                return false;

            return true;
        }
        public static async Task<List<JobMasterItem>> GetJobMasterAsync(string eqptCode)
        {
            var resp = await _client.GetAsync($"cds/job-master/{eqptCode}");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<JobMasterItem>>(json)
                   ?? new List<JobMasterItem>();
        }

        public static async Task<bool> AddJobMasterAsync(JobMasterPayload payload)
        {
            var resp = await _client.PostAsJsonAsync("cds/job-master", payload);

            if (!resp.IsSuccessStatusCode)
                return false;

            return true;
        }
        public static async Task<List<JobMasterItem>> GetJobsAsync(string eqptCode)
        {
            var resp = await _client.GetAsync($"cds/job-master/{eqptCode}");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<JobMasterItem>>(json)
                   ?? new List<JobMasterItem>();
        }

        public static async Task<List<LPRItem>> GetLPRListAsync()
        {
            var resp = await _client.GetAsync("lpr/");
            resp.EnsureSuccessStatusCode();

            var json = await resp.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<List<LPRItem>>(json)
                   ?? new List<LPRItem>();
        }

        public static async Task<bool> ForgetPasswordAsync(string username, string newPassword)
        {
            var payload = new
            {
                username = username,
                new_password = newPassword
            };

            var resp = await _client.PostAsJsonAsync("forget-password", payload);

            if (!resp.IsSuccessStatusCode)
                return false;

            return true;
        }

        public static async Task<bool> CreateDemandAsync(DemandCreate payload)
        {
            var resp = await _client.PostAsJsonAsync("demand/", payload);
            return resp.IsSuccessStatusCode;
        }

        public static async Task<List<DemandResponse>> GetAllDemandsAsync()
        {
            var resp = await _client.GetAsync("demand/");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
                   ?? new List<DemandResponse>();
        }

        public static async Task<List<DemandResponse>> GetDemandByNoAsync(int demandNo)
        {
            var resp = await _client.GetAsync($"demand/{demandNo}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DemandResponse>>()
                   ?? new List<DemandResponse>();
        }
        public static async Task<bool> DeleteDemandAsync(int demandNo)
        {
            var resp = await _client.DeleteAsync($"demand/{demandNo}");
            return resp.IsSuccessStatusCode;
        }
        public static async Task<bool> LockDemandAsync(int demandNo)
        {
            var resp = await _client.PostAsync($"demand/{demandNo}/lock", null);
            return resp.IsSuccessStatusCode;
        }
        public static async Task<bool> UnlockDemandAsync(int demandNo)
        {
            var resp = await _client.PostAsync($"demand/{demandNo}/unlock", null);
            return resp.IsSuccessStatusCode;
        }
        public static async Task<List<DmdJunctionCreate>> GetDemandDetailsAsync(int demandNo)
        {
            var resp = await _client.GetAsync($"demand/detail/{demandNo}");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<DmdJunctionCreate>>()
                   ?? new List<DmdJunctionCreate>();
        }
        public static async Task<List<EquipmentResponse>> GetAllEquipmentsAsync()
        {
            var resp = await _client.GetAsync("demand/equipments/");
            resp.EnsureSuccessStatusCode();

            return await resp.Content.ReadFromJsonAsync<List<EquipmentResponse>>()
                   ?? new List<EquipmentResponse>();
        }


    }
}
