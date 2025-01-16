document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("gitgraph-container");
    const gitgraph = GitgraphJS.createGitgraph(container);

    // Add branches and commits
    const master = gitgraph.branch("main");
    master.commit("Initial commit");

    const feature = gitgraph.branch("feature-1");
    feature.commit("Add new feature");

    master.merge(feature, "Merge feature-1");
});
