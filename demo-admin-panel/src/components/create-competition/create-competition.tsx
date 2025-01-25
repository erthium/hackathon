import { useMutation } from "@tanstack/react-query";
import { SubmitHandler, useForm } from "react-hook-form";

type CreateCompetitionInputs = {
  name: string;
  start_date: Date;
  end_date: Date;
};

export function CreateCompetition() {
  const { register, handleSubmit } = useForm<CreateCompetitionInputs>();

  const createTeamMutation = useMutation({
    mutationFn: async (data: CreateCompetitionInputs) => {
      const resp = await fetch("/api/competition/create", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!resp.ok) {
        throw new Error(JSON.stringify(await resp.json()));
      }
    },
    onSuccess: (data) => {
      console.log(data);
    },
    onError: (error) => {
      console.error(error);
    },
  });

  const onSubmit: SubmitHandler<CreateCompetitionInputs> = async (data) => {
    createTeamMutation.mutate(data);
  };

  return (
    <form className="form-control gap-5" onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-col gap-1">
        <label>
          <div className="label">
            <span className="label-text">Competition Name</span>
          </div>
          <input
            type="text"
            className="input input-bordered w-full"
            {...register("name", { required: true })}
          />
        </label>

        <div className="flex gap-3 [&>*]:flex-1">
          <label>
            <div className="label">
              <span className="label-text">Start Date</span>
            </div>
            <input
              type="datetime-local"
              className="input input-bordered w-full"
              {...register("start_date", { required: true })}
            />
          </label>

          <label>
            <div className="label">
              <span className="label-text">End Date</span>
            </div>
            <input
              type="datetime-local"
              className="input input-bordered w-full"
              {...register("end_date", { required: true })}
            />
          </label>
        </div>
      </div>

      <button className="btn btn-success">Create Competition</button>
    </form>
  );
}
