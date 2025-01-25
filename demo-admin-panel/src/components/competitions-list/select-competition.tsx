import { Competition } from "@/types";

type SelectCompetitionProps = {
  competitions: Competition[];
  selectedCompetitionId?: Competition["id"];
  onSelect: (competitionId: Competition["id"]) => void;
};

export function SelectCompetition(props: SelectCompetitionProps) {
  return (
    <select
      className="select select-bordered w-full"
      defaultValue={props.selectedCompetitionId}
      onChange={(event) =>
        props.onSelect(event.target.value as Competition["id"])
      }
    >
      {props.competitions.map((competition) => (
        <option key={competition.id} value={competition.id}>
          {competition.name}
        </option>
      ))}
    </select>
  );
}
