module.exports = function (plop) {
  plop.setGenerator("component", {
    description: "Create a new React component",
    prompts: [
      {
        type: "input",
        name: "name",
        message: "Component name?",
      },
    ],
    actions: [
      {
        type: "add",
        path: "src/components/{{camelCase name}}/{{pascalCase name}}.tsx",
        templateFile: "plop-templates/Component.tsx.hbs",
      },
      {
        type: "add",
        path: "src/components/{{camelCase name}}/{{pascalCase name}}.css",
        templateFile: "plop-templates/Component.css.hbs",
      },
      {
        type: "modify",
        path: "src/components/index.tsx",
        pattern: /(\/\/ COMPONENT EXPORTS)/,
        template: `export { default as {{pascalCase name}} } from './{{camelCase name}}/{{pascalCase name}}';\n$1`,
      },
    ],
  });

  plop.setGenerator("container", {
    description: "Create a new React container",
    prompts: [
      {
        type: "input",
        name: "name",
        message: "Container name?",
      },
    ],
    actions: [
      {
        type: "add",
        path: "src/containers/{{camelCase name}}/{{pascalCase name}}.tsx",
        templateFile: "plop-templates/Container.tsx.hbs",
      },
      {
        type: "add",
        path: "src/containers/{{camelCase name}}/{{pascalCase name}}.css",
        templateFile: "plop-templates/Container.css.hbs",
      },
      {
        type: "modify",
        path: "src/containers/index.tsx",
        pattern: /(\/\/ CONTAINER EXPORTS)/,
        template: `export { default as {{pascalCase name}} } from './{{camelCase name}}/{{pascalCase name}}';\n$1`,
      },
    ],
  });
};
