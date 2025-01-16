document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("gitgraph-container");
    const gitgraph = GitgraphJS.createGitgraph(container);

    // Example dynamic data (replace with real data from your backend)
    const repoName = container.dataset.repoName;
    const branches = JSON.parse(container.dataset.repoData); // Assuming backend passes JSON data

    // Populate the graph
    const branchObjects = {};
    for (const [branchName, branchData] of Object.entries(branches)) {
        branchObjects[branchName] = gitgraph.branch(branchName);
        branchData.commits.forEach(commit => {
            branchObjects[branchName].commit(commit.message);
        });

        // If the branch has a target PR, draw a dotted connection
        if (branchData.target_pr) {
            gitgraph.branch(branchData.target_pr).merge(branchObjects[branchName], "PR merge");
        }
    }

    // Slow scroll to the bottom where branch heads are located
    setTimeout(() => {
        container.scrollTo({
            top: container.scrollHeight,
            behavior: "smooth",
        });
    }, 500); // Delay to ensure rendering is complete
});
