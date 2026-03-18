const std = @import("std");
const zine = @import("zine");

pub fn build(b: *std.Build) void {
    const website = zine.website(b, .{});
    b.getInstallStep().dependOn(&website.step);

    const serve = zine.serve(b, .{});
    serve.addArg("serve"); // workaround: zine.serve() missing addArg("serve") in v0.11.2
    const serve_step = b.step("serve", "Run the local development server");
    serve_step.dependOn(&serve.step);
}
