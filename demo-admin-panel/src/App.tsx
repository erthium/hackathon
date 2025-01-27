import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./App.css";
import { Layout } from "./pages/layout";
import { SubmissionsPage } from "./pages/submissions";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <SubmissionsPage />
      </Layout>
    </QueryClientProvider>
  );
}

export default App;
