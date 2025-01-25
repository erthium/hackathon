import { CompetitionsList } from "@/components/competitions-list";
import { CreateCompetition } from "@/components/create-competition";

export function CompetitionsPage() {
  return (
    <div className="flex flex-1 items-center justify-center gap-5">
      <div className="flex flex-1 justify-center max-xl:flex-col max-xl:items-stretch">
        <CreateCompetition />

        <div className="divider divider-horizontal max-xl:divider-vertical" />

        <div className="min-xl:max-w-4xl">
          <CompetitionsList />
        </div>
      </div>
    </div>
  );
}
