### 📄 **Workflow Modification Policy**

1. **Soft Reset Notice**
   A soft reset will be applied to all changes made under the `.github/workflows/` directory. These workflow adjustments will be re-implemented manually by the maintainer.

2. **Change Management**
   Any future edits, enhancements, or refactors to workflow files **must not be submitted as pull requests**.
   Instead, please **open an issue** describing:

   * The purpose of the change,
   * The affected workflow(s), and
   * The intended impact or expected outcome.

3. **Rationale**
   CI/CD configurations in `.github/workflows/` are critical to repository security and deployment stability. All changes will therefore be reviewed and applied manually to maintain configuration integrity.

4. **Contributor Action**

   * Do **not** push workflow changes directly.
   * Do **not** open PRs altering `.github/workflows/**`.
   * Use the “Issues” tab to propose workflow-related modifications.
