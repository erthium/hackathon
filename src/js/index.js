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
    //   name: "deneme3",
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
    // await octokit.request('POST /repos/{owner}/{repo}/releases', {
    //   owner: 'OWNER',
    //   repo: 'REPO',
    //   tag_name: 'v1.0.0',
    //   target_commitish: 'master',
    //   name: 'v1.0.0',
    //   body: 'Description of the release',
    //   draft: false,
    //   prerelease: false,
    //   generate_release_notes: false,
    //   headers: {
    //     'X-GitHub-Api-Version': '2022-11-28'
    //   }
    // })
    const releases = await octokit.request("GET /repos/{owner}/{repo}/releases", {
        owner: organization,
        repo: "deneme3",
        headers: {
            "X-GitHub-Api-Version": "2022-11-28",
        },
    });
    console.log(releases);
}
main();
