import { Competition } from "@/types";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { AddTeams } from "../add-teams";
import { SelectCompetition } from "./select-competition";

export function CompetitionsList() {
  const competitionsQuery = useQuery({
    queryKey: ["competitions"],
    queryFn: async () => {
      const response = await fetch("/api/competition/all");
      return (await response.json()) as { competitions: Competition[] };
    },
  });

  const [selectedCompetitionId, setSelectedCompetitionId] =
    useState<Competition["id"]>();

  const selectedCompetition = competitionsQuery.data?.competitions.find(
    (competition) => competition.id === selectedCompetitionId,
  );

  useEffect(() => {
    if (competitionsQuery.isSuccess) {
      setSelectedCompetitionId(competitionsQuery.data.competitions[0].id);
    }
  }, [competitionsQuery.data?.competitions, competitionsQuery.isSuccess]);

  return (
    <div className="w-full">
      {competitionsQuery.isLoading && <p>Loading...</p>}
      {competitionsQuery.isError && (
        <p>Error: {competitionsQuery.error.message}</p>
      )}
      {competitionsQuery.isSuccess && (
        <div className="grid gap-4">
          <SelectCompetition
            competitions={competitionsQuery.data.competitions}
            onSelect={setSelectedCompetitionId}
            selectedCompetitionId={selectedCompetitionId}
          />

          {selectedCompetition !== undefined && (
            <div className="card bg-base-300 shadow-xl">
              <div className="card-body">
                <div className="card-title">Teams</div>
                <AddTeams competition_id={selectedCompetition.id} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
