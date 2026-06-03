import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerTitle: "CBBS Client",
        headerStyle: { backgroundColor: "#111827" },
        headerTintColor: "#F8FAFC"
      }}
    />
  );
}
