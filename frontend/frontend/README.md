# IMS Frontend (WPF / .NET 8)

This folder contains the **Windows Presentation Foundation (WPF)** frontend for the IMS project.
The project uses .NET 8 and includes a Windows Application Packaging (WAP) project for MSIX builds,
along with a unit test project for automated testing.

---

## 📁 Project Structure

```

frontend/
├── IMS.sln                     # Solution entry point
├── IMS/                        # Main WPF app (UI + logic)
│   ├── App.xaml
│   ├── MainWindow.xaml
│   └── IMS.csproj
├── IMS.Package/                # Windows Application Packaging project
│   └── IMS.Package.wapproj
test/
└── frontend_tests/              # Unit test project
    └── IMS.Tests.csproj

---

## 🧱 Prerequisites

- Windows 10/11
- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Visual Studio 2022 (with “Desktop development with .NET” workload) or command line .NET tools

---

## ⚙️ Initial Project Setup

Run these commands from the repository root:

```bash
cd frontend

# 1. Create main WPF app
dotnet new wpf -n IMS

# 2. Create Windows Application Packaging (WAP) project
dotnet new wapproj -n IMS.Package

# 3. Create test project (MSTest)
cd tests
dotnet new mstest -n frontend_tests
cd ..

# 4. Create solution and add all projects
dotnet new sln -n IMS
dotnet sln IMS.sln add IMS/IMS.csproj
dotnet sln IMS.sln add IMS.Package/IMS.Package.wapproj
dotnet sln IMS.sln add tests/frontend_tests/IMS.Tests.csproj

# 5. Reference the main app in test project
dotnet add tests/IMS.Tests/IMS.Tests.csproj reference IMS/IMS.csproj
````

After these steps, the directory layout will match what the CI workflow expects.

---

## 🧩 Environment Variables in CI

The GitHub Actions workflow uses these environment variables:

| Variable                | Description                   | Example                                     |
| ----------------------- | ----------------------------- | ------------------------------------------- |
| `Solution_Name`         | Path to the solution file     | `frontend/IMS.sln`                          |
| `Test_Project_Path`     | Path to test project          | `tests/frontend_tests/IMS.Tests.csproj` |
| `Wap_Project_Directory` | Folder containing WAP project | `frontend/IMS.Package`                      |
| `Wap_Project_Path`      | Full path to `.wapproj`       | `frontend/IMS.Package/IMS.Package.wapproj`  |
| `Configuration`         | Build configuration           | `Release`                                   |

---

## 🧪 Build, Test, and Package Locally

```bash
# Restore dependencies
dotnet restore IMS.sln

# Build in Release mode
dotnet build IMS.sln -c Release

# Run unit tests
dotnet test tests/IMS.Tests/IMS.Tests.csproj -c Release

# Build MSIX package (unsigned)
dotnet msbuild IMS.Package/IMS.Package.wapproj /p:Configuration=Release /t:Build,Publish
```
Output packages (.msix or .msixbundle) will appear under:
```
frontend/IMS.Package/bin/Release/
```
