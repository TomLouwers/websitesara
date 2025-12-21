#!/usr/bin/env node

/**
 * Test migration on a single file
 *
 * Usage:
 *   node scripts/test-single-file.js data/exercises/bl/bl_groep4_m4_1.json
 */

const fs = require('fs');
const path = require('path');

const transformBL = require('./transformers/bl-transformer');
const transformGB = require('./transformers/gb-transformer');
const transformWO = require('./transformers/wo-transformer');
const transformWS = require('./transformers/ws-transformer');
const transformSP = require('./transformers/sp-transformer');
const transformTL = require('./transformers/tl-transformer');

const { validateCore, validateSupport } = require('./validators/schema-validator');

const TRANSFORMERS = {
  bl: transformBL,
  gb: transformGB,
  wo: transformWO,
  ws: transformWS,
  sp: transformSP,
  tl: transformTL,
};

// Get file path from command line
const filePath = process.argv[2];

if (!filePath) {
  console.error('Usage: node test-single-file.js <path-to-json-file>');
  console.error('Example: node test-single-file.js data/exercises/bl/bl_groep4_m4_1.json');
  process.exit(1);
}

if (!fs.existsSync(filePath)) {
  console.error(`File not found: ${filePath}`);
  process.exit(1);
}

// Detect category from path
const category = filePath.match(/\/(bl|gb|wo|ws|sp|tl)\//)?.[1];

if (!category) {
  console.error('Could not detect category from path. Expected path like: data/exercises/bl/file.json');
  process.exit(1);
}

const transformer = TRANSFORMERS[category];

if (!transformer) {
  console.error(`No transformer for category: ${category}`);
  process.exit(1);
}

console.log(`\n🧪 Testing migration for: ${filePath}`);
console.log(`Category: ${category}\n`);

try {
  // Read file
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const filename = path.basename(filePath);

  console.log('📖 Original data:');
  console.log(JSON.stringify(data, null, 2).substring(0, 500) + '...\n');

  // Transform
  console.log('🔄 Transforming...');
  const { core, support } = transformer(data, filename);

  // Validate
  console.log('\n✅ Core data:');
  console.log(JSON.stringify(core, null, 2));

  console.log('\n✅ Support data:');
  console.log(JSON.stringify(support, null, 2));

  // Run validation
  console.log('\n🔍 Validating...');
  const coreValidation = validateCore(core);
  const supportValidation = validateSupport(support);

  if (coreValidation.valid) {
    console.log('✅ Core validation: PASSED');
  } else {
    console.log('❌ Core validation: FAILED');
    console.log('Errors:', coreValidation.errors);
  }

  if (supportValidation.valid) {
    console.log('✅ Support validation: PASSED');
  } else {
    console.log('❌ Support validation: FAILED');
    console.log('Errors:', supportValidation.errors);
  }

  // Summary
  console.log('\n📊 Summary:');
  console.log(`Source items: ${getItemCount(data, category)}`);
  console.log(`Core items: ${core.items?.length || 0}`);
  console.log(`Support items: ${support.items?.length || 0}`);

  if (coreValidation.valid && supportValidation.valid) {
    console.log('\n✅ Migration test PASSED!\n');
    process.exit(0);
  } else {
    console.log('\n❌ Migration test FAILED!\n');
    process.exit(1);
  }

} catch (error) {
  console.error('\n❌ Error:', error.message);
  console.error(error.stack);
  process.exit(1);
}

function getItemCount(data, category) {
  switch (category) {
    case 'bl':
      return Array.isArray(data) ? data[0]?.questions?.length : data.questions?.length || 0;
    case 'gb':
    case 'wo':
    case 'ws':
      return Array.isArray(data) ? data.length : 1;
    case 'sp':
      return data.items?.length || 0;
    case 'tl':
      return data.list?.words?.length || 0;
    default:
      return 0;
  }
}
