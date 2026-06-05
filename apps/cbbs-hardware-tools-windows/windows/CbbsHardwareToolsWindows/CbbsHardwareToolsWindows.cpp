// CbbsHardwareToolsWindows.cpp : Defines the entry point for the application.
//

#include "pch.h"
#include "CbbsHardwareToolsWindows.h"

#include "AutolinkedNativeModules.g.h"

#include "NativeModules.h"

#include <algorithm>

namespace {

constexpr int32_t kMinimumStartupWidth = 960;
constexpr int32_t kMinimumStartupHeight = 640;
constexpr int32_t kPreferredStartupWidth = 1440;
constexpr int32_t kPreferredStartupHeight = 900;
constexpr int32_t kWorkAreaInset = 96;

int32_t startup_extent(int32_t preferred, int32_t minimum, int32_t workAreaExtent) noexcept {
  if (workAreaExtent <= 0) {
    return preferred;
  }

  const int32_t insetExtent = workAreaExtent > kWorkAreaInset ? workAreaExtent - kWorkAreaInset : workAreaExtent;
  return std::max(std::min(preferred, insetExtent), std::min(minimum, insetExtent));
}

void ConfigureHardwareToolsStartupWindow(
    winrt::Microsoft::UI::Windowing::AppWindow const &appWindow) noexcept {
  appWindow.Title(L"CbbsHardwareToolsWindows");

  try {
    const auto displayArea = winrt::Microsoft::UI::Windowing::DisplayArea::GetFromWindowId(
        appWindow.Id(), winrt::Microsoft::UI::Windowing::DisplayAreaFallback::Primary);
    const auto workArea = displayArea.WorkArea();
    appWindow.Resize({
        startup_extent(kPreferredStartupWidth, kMinimumStartupWidth, workArea.Width),
        startup_extent(kPreferredStartupHeight, kMinimumStartupHeight, workArea.Height)});

    if (const auto presenter =
            appWindow.Presenter().try_as<winrt::Microsoft::UI::Windowing::OverlappedPresenter>()) {
      presenter.Maximize();
    }
  } catch (...) {
    appWindow.Resize({kMinimumStartupWidth, kMinimumStartupHeight});
  }
}

} // namespace

// A PackageProvider containing any turbo modules you define within this app project
struct CompReactPackageProvider
    : winrt::implements<CompReactPackageProvider, winrt::Microsoft::ReactNative::IReactPackageProvider> {
 public: // IReactPackageProvider
  void CreatePackage(winrt::Microsoft::ReactNative::IReactPackageBuilder const &packageBuilder) noexcept {
    AddAttributedModules(packageBuilder, true);
  }
};

// The entry point of the Win32 application
_Use_decl_annotations_ int CALLBACK WinMain(HINSTANCE instance, HINSTANCE, PSTR /* commandLine */, int showCmd) {
  // Initialize WinRT
  winrt::init_apartment(winrt::apartment_type::single_threaded);

  // Enable per monitor DPI scaling
  SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);

  // Find the path hosting the app exe file
  WCHAR appDirectory[MAX_PATH];
  GetModuleFileNameW(NULL, appDirectory, MAX_PATH);
  PathCchRemoveFileSpec(appDirectory, MAX_PATH);

  // Create a ReactNativeWin32App with the ReactNativeAppBuilder
  auto reactNativeWin32App{winrt::Microsoft::ReactNative::ReactNativeAppBuilder().Build()};

  // Configure the initial InstanceSettings for the app's ReactNativeHost
  auto settings{reactNativeWin32App.ReactNativeHost().InstanceSettings()};
  // Register any autolinked native modules
  RegisterAutolinkedNativeModulePackages(settings.PackageProviders());
  // Register any native modules defined within this app project
  settings.PackageProviders().Append(winrt::make<CompReactPackageProvider>());

#if BUNDLE
  // Load the JS bundle from a file (not Metro):
  // Set the path (on disk) where the .bundle file is located
  settings.BundleRootPath(std::wstring(L"file://").append(appDirectory).append(L"\\Bundle\\").c_str());
  // Set the name of the bundle file (without the .bundle extension)
  settings.JavaScriptBundleFile(L"index.windows");
  // Disable hot reload
  settings.UseFastRefresh(false);
#else
  // Load the JS bundle from Metro
  settings.JavaScriptBundleFile(L"index");
  // Enable hot reload
  settings.UseFastRefresh(true);
#endif
#if _DEBUG
  // For Debug builds
  // Enable Direct Debugging of JS
  settings.UseDirectDebugger(true);
  // Enable the Developer Menu
  settings.UseDeveloperSupport(true);
#else
  // For Release builds:
  // Disable Direct Debugging of JS
  settings.UseDirectDebugger(false);
  // Disable the Developer Menu
  settings.UseDeveloperSupport(false);
#endif

  // Get the AppWindow so we can configure its initial title and size
  auto appWindow{reactNativeWin32App.AppWindow()};
  ConfigureHardwareToolsStartupWindow(appWindow);

  // Get the ReactViewOptions so we can set the initial RN component to load
  auto viewOptions{reactNativeWin32App.ReactViewOptions()};
  viewOptions.ComponentName(L"CbbsHardwareToolsWindows");

  // Start the app
  reactNativeWin32App.Start();
}
