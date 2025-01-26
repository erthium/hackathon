import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./App.css";
import { CompetitionsPage } from "./pages";
import { Layout } from "./pages/layout";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Layout>
        <CompetitionsPage />
      </Layout>
    </QueryClientProvider>
  );
}

export default App;
