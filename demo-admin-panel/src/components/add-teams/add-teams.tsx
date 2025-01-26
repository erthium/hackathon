import { useMutation } from "@tanstack/react-query";
import {
  Control,
  SubmitHandler,
  useFieldArray,
  useForm,
  UseFormRegister,
} from "react-hook-form";

type AddTeamsProps = {
  competition_id: string;
};

type AddTeamsInputs = {
  teams: {
    name: string;
    members: {
      github_username: string;
      email: string;
    }[];
  }[];
};

export function AddTeams({ competition_id }: AddTeamsProps) {
  const { register, handleSubmit, control } = useForm<AddTeamsInputs>();

  const { fields, append } = useFieldArray({
    control, // control props comes from useForm (optional: if you are using FormProvider)
    name: "teams", // unique name for your Field Array
  });

  const addTeamsMutation = useMutation({
    mutationFn: async (data: AddTeamsInputs) => {
      const resp = await fetch("/api/competition/add_teams", {
        method: "POST",
        body: JSON.stringify({ competition_id, ...data }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!resp.ok) {
        throw await resp.json();
      }
    },
    onSuccess: (data) => {
      console.log(data);
    },
    onError: (error) => {
      console.error(error);

      if ("detail" in error) {
        console.error(error.detail);
      }
    },
  });

  const onSubmit: SubmitHandler<AddTeamsInputs> = async (data) => {
    console.log(data);

    addTeamsMutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="max-h-96 overflow-auto">
        {fields.length === 0 && (
          <p className="text-center italic text-neutral">No teams added yet</p>
        )}

        {fields.length > 0 && (
          <table className="table [&_tr]:border-neutral">
            <thead>
              <tr>
                <th />
                <th>Name</th>
                <th>Members</th>
              </tr>
            </thead>
            <tbody>
              {fields.map((field, index) => (
                <tr key={field.id}>
                  <th>{index + 1}</th>
                  <td>
                    <input
                      {...register(`teams.${index}.name`, { required: true })}
                      className="input input-md input-bordered w-40"
                    />
                  </td>
                  <td>
                    <MembersTable
                      register={register}
                      control={control}
                      teamIndex={index}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div className="flex justify-center pt-3">
          <button
            type="button"
            onClick={() =>
              append({
                name: "",
                members: [{ email: "", github_username: "" }],
              })
            }
            className="btn btn-primary"
          >
            +
          </button>
        </div>
      </div>

      <button type="submit" className="btn btn-secondary float-right mt-3">
        Add Teams
      </button>
    </form>
  );
}

type MembersTableProps = {
  register: UseFormRegister<AddTeamsInputs>;
  control: Control<AddTeamsInputs>;
  teamIndex: number;
};

function MembersTable(props: MembersTableProps) {
  const { fields: innerFields, append } = useFieldArray({
    control: props.control,
    name: `teams.${props.teamIndex}.members`, // unique name for your Field Array
  });
  return (
    <>
      <table className="table">
        <thead>
          <tr>
            <th>GitHub Username</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {innerFields.map((member, memberIndex) => (
            <tr key={member.github_username + memberIndex}>
              <td>
                <input
                  {...props.register(
                    `teams.${props.teamIndex}.members.${memberIndex}.github_username`,
                    { required: true },
                  )}
                  className="input input-sm input-bordered w-40"
                />
              </td>
              <td>
                <input
                  {...props.register(
                    `teams.${props.teamIndex}.members.${memberIndex}.email`,
                    { required: true },
                  )}
                  className="input input-sm input-bordered w-40"
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-center pt-3">
        <button
          type="button"
          onClick={() => append({ email: "", github_username: "" })}
          className="btn btn-primary"
        >
          +
        </button>
      </div>
    </>
  );
}
