const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

const path = require('node:path');

const appRoot = path.resolve(__dirname);
const workspaceRoot = path.resolve(appRoot, '../..');
const appNodeModules = path.resolve(appRoot, 'node_modules');
const workspaceNodeModules = path.resolve(workspaceRoot, 'node_modules');
const cbbsProtocolPath = path.resolve(workspaceRoot, 'packages/cbbs-protocol');
const cbbsProductPath = path.resolve(workspaceRoot, 'packages/cbbs-product');
const cbbsProductUiPath = path.resolve(workspaceRoot, 'packages/cbbs-product-ui');
const rnwPath = path.resolve(
  path.resolve(require.resolve('react-native-windows/package.json'), '..'),
);
const reactDevToolsSettingsManagerPath = path.resolve(
  appRoot,
  'metro-shims/reactDevToolsSettingsManager.windows.js',
);
const reactPath = path.resolve(
  path.resolve(require.resolve('react/package.json'), '..'),
);
const reactNativePath = path.resolve(
  path.resolve(require.resolve('react-native/package.json'), '..'),
);

//

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 *
 * @type {import('metro-config').MetroConfig}
 */

const config = {
  watchFolders: [
    workspaceNodeModules,
    cbbsProductPath,
    cbbsProductUiPath,
    cbbsProtocolPath,
  ],
  //
  resolver: {
    disableHierarchicalLookup: true,
    resolveRequest: (context, moduleName, platform) => {
      if (platform === 'windows' && moduleName === 'react-native') {
        return {
          type: 'sourceFile',
          filePath: path.join(rnwPath, 'index.windows.js'),
        };
      }

      if (platform === 'windows' && moduleName.startsWith('react-native/')) {
        return context.resolveRequest(
          context,
          path.join(rnwPath, moduleName.slice('react-native/'.length)),
          platform,
        );
      }

      if (
        platform === 'windows' &&
        moduleName
          .replace(/\\/g, '/')
          .endsWith('src/private/devsupport/rndevtools/ReactDevToolsSettingsManager')
      ) {
        return {
          type: 'sourceFile',
          filePath: reactDevToolsSettingsManagerPath,
        };
      }

      return context.resolveRequest(context, moduleName, platform);
    },
    extraNodeModules: {
      react: reactPath,
      'react-native': reactNativePath,
      'react-native-windows': rnwPath,
      '@cbbs/product': cbbsProductPath,
      '@cbbs/product-ui': cbbsProductUiPath,
      '@cbbs/protocol': cbbsProtocolPath,
    },
    nodeModulesPaths: [
      appNodeModules,
      workspaceNodeModules,
    ],
    blockList: [
      // Keep the generated native tree out of Metro's file watcher.
      new RegExp(
        `${path.resolve(appRoot, 'windows').replace(/[/\\]/g, '/')}.*`,
      ),
      // Keep generated RNW build intermediates out of Metro's file watcher.
      new RegExp(`${rnwPath}/build/.*`),
      new RegExp(`${rnwPath}/target/.*`),
      /.*\.ProjectImports\.zip/,
    ],
    //
  },
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },
};

module.exports = mergeConfig(getDefaultConfig(appRoot), config);
