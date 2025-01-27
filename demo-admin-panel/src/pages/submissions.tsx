import { Submission } from "@/types";
import { useQuery } from "@tanstack/react-query";

export function SubmissionsPage() {
  const submissionsQuery = useQuery({
    queryKey: ["submissions"],
    queryFn: async () => {
      const response = await fetch("/api/release/all");
      return (await response.json()) as Submission[];
    },
  });

  return (
    <div className="w-full">
      {submissionsQuery.isLoading && <p>Loading...</p>}
      {submissionsQuery.isError && (
        <p>Error: {submissionsQuery.error.message}</p>
      )}
      {submissionsQuery.isSuccess && (
        <table className="table w-full [&_tr]:border-neutral">
          <thead>
            <tr>
              <th>Team</th>
              <th>Commit</th>
              <th>Status</th>
              <th>Message</th>
              <th>Score</th>
              <th>Release Date</th>
            </tr>
          </thead>
          <tbody>
            {submissionsQuery.data.map((submission) => (
              <tr key={submission.id}>
                <td>{submission.team_id}</td>
                <td>{submission.commit_id}</td>
                <td>{submission.status}</td>
                <td>{submission.message}</td>
                <td>{submission.score}</td>
                <td>{submission.release_date.toLocaleString("tr")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
