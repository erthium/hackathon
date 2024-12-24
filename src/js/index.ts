import { Octokit } from "@octokit/core";

const octokit = new Octokit({
  auth: "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",
});

async function main() {
  const organization = "ituai-deneme";
  const headers = {
    "X-GitHub-Api-Version": "2022-11-28",
  };
  // const res = await octokit.request("GET /orgs/{org}/hooks", {
  //   org: organization,
  //   headers,
  // });

  // const hookId = res.data[0].id;

  // const hook = await octokit.request("GET /orgs/{org}/hooks/{hook_id}", {
  //   org: organization,
  //   hook_id: hookId,
  //   headers: {
  //     "X-GitHub-Api-Version": "2022-11-28",
  //   },
  // });

  // const deliveries = await octokit.request(
  //   "GET /orgs/{org}/hooks/{hook_id}/deliveries",
  //   {
  //     org: organization,
  //     hook_id: hookId,
  //     headers: {
  //       "X-GitHub-Api-Version": "2022-11-28",
  //     },
  //   }
  // );

  // const erroneousDeliveries = deliveries.data.filter(
  //   (delivery) => !delivery.redelivery && delivery.status_code !== 200
  // );

  // console.log(erroneousDeliveries);

  // await octokit.request("POST /orgs/{org}/repos", {
  //   org: organization,
  //   name: "deneme6",
  //   description: "deneme",
  //   homepage: "https://github.com",
  //   private: false,
  //   has_issues: true,
  //   has_projects: true,
  //   has_wiki: true,
  //   headers: {
  //     "X-GitHub-Api-Version": "2022-11-28",
  //   },
  // });

  // const releases = await octokit.request("GET /repos/{owner}/{repo}/releases", {
  //   owner: organization,
  //   repo: "deneme3",
  //   headers: {
  //     "X-GitHub-Api-Version": "2022-11-28",
  //   },
  // });
  // console.log(releases);

  // await octokit.request("POST /repos/{owner}/{repo}/releases", {
  //   owner: organization,
  //   repo: "deneme3",
  //   tag_name: "v1.0.0",
  //   // target_commitish: "main",
  //   name: "v1.0.0",
  //   body: "deneme",
  //   draft: false,
  //   prerelease: false,
  //   generate_release_notes: false,
  //   headers: {
  //     "X-GitHub-Api-Version": "2022-11-28",
  //   },
  // });

  // await octokit.request(
  //   "POST /repos/{template_owner}/{template_repo}/generate",
  //   {
  //     template_owner: "brkdnmz",
  //     template_repo: "wordle-plus-plus",
  //     owner: "ituai-deneme",
  //     name: "deneme10",
  //     description: "This is your first repository",
  //     include_all_branches: false,
  //     private: true,
  //     headers: {
  //       "X-GitHub-Api-Version": "2022-11-28",
  //     },
  //   }
  // );

  // console.log(
  //   await octokit.request(
  //     "GET /repos/{owner}/{repo}/collaborators/{username}",
  //     {
  //       owner: "ituai-deneme",
  //       repo: "deneme2",
  //       username: "brkdnmz",
  //       headers: {
  //         "X-GitHub-Api-Version": "2022-11-28",
  //       },
  //     }
  //   )
  // );

  // console.log(
  //   await octokit.request(
  //     "PUT /repos/{owner}/{repo}/collaborators/{username}",
  //     {
  //       owner: "ituai-deneme",
  //       repo: "deneme2",
  //       username: "brkdnmz",
  //       permission: "admin",
  //       headers: {
  //         "X-GitHub-Api-Version": "2022-11-28",
  //       },
  //     }
  //   )
  // );

  // console.log(
  //   await octokit.request("POST /repos/{owner}/{repo}/hooks", {
  //     owner: "ituai-deneme",
  //     repo: "deneme2",
  //     name: "web",
  //     active: true,
  //     events: ["push", "release"],
  //     config: {
  //       url: "https://imp-patient-evidently.ngrok-free.app/github/webhook",
  //       content_type: "json",
  //       insecure_ssl: "0",
  //     },
  //     headers: {
  //       "X-GitHub-Api-Version": "2022-11-28",
  //     },
  //   })
  // );
}

main();
