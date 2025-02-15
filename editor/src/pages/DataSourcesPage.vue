<template>
    <div>
        <div v-if="doc != null" class="back-to-top">
            <label @click="navigateToTop" class="cursor-pointer" title="Back to top">
                <icons icon="arrow-up"></icons>
            </label>
        </div>

        <div class="row" id="pageTop">
            <div class="col">
                <div class="card card-card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="tim-icons icon-coins"></i> Data Sources</h2>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col">
                                <button type="button" class="btn mr-md-3" @click="askNewFile">
                                    <icons icon="file-empty"></icons>
                                    &nbsp;New file
                                </button>
                                <label class="custom-file-upload">
                                    <icons icon="file"></icons>
                                    &nbsp;Select YAML file
                                    <file-reader @load="readFile($event)" :setFileNameFn="setFileName" :id="'dsFileReader'"></file-reader>
                                </label>
                                <label v-if="fileChanged" class="pl-2">
                                    <icons icon="text-balloon"></icons>
                                    You have unsaved changes. You may want to save the file to preserve your changes.</label
                                >
                            </div>
                        </div>
                        <div v-if="doc != null" class="row pt-md-2">
                            <div class="col">
                                <file-details :filename="filename" :doc="doc" :platforms="platforms"></file-details>
                            </div>
                        </div>
                        <div v-if="doc != null" class="row">
                            <div class="col">
                                <div class="row">
                                    <button type="button" class="btn mr-md-3" @click="downloadYaml('data_sources', 'data_source_name')">
                                        <icons icon="save"></icons>
                                        &nbsp;Save YAML file
                                    </button>
                                    <label class="btn ml-mr-0">
                                        <icons icon="file"></icons>
                                        &nbsp;Fill from log files
                                        <input type="file" multiple accept="text/xml" @change="readLogFiles" style="opacity: 0">
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="doc != null" class="row">
            <div class="col">
                <card type="card">
                    <div class="row">
                        <div class="col">
                            <p>
                                <button
                                    type="button"
                                    class="btn btn-secondary"
                                    @click="addItem('data_sources', 'data_source_name', emptyDataSourceObject)"
                                >
                                    <icons icon="plus"></icons>
                                    &nbsp;Add data source
                                </button>
                            </p>
                        </div>
                    </div>
                    <div class="row mt-md-2">
                        <div class="col">
                            <base-input v-model="filters.filter.value" placeholder="filter" />
                            <v-table
                                :data="doc.data_sources"
                                @selectionChanged="selectItem($event)"
                                selectedClass="table-selected-custom"
                                :filters="filters"
                                class="table-custom"
                                ref="data_table"
                            >
                                <thead slot="head">
                                    <v-th sortKey="data_source_name" defaultSort="asc" width="350">Name</v-th>
                                    <v-th sortKey="date_registered" width="200">Date registered</v-th>
                                    <v-th sortKey="products" width="350">Products</v-th>
                                    <th></th>
                                </thead>
                                <tbody slot="body" slot-scope="{ displayData }">
                                    <v-tr v-for="(row, i) in displayData" :key="row.data_source_name" :row="row" ref="data_table_rows">
                                        <td>{{ row.data_source_name }}</td>
                                        <td>{{ row.date_registered }}</td>
                                        <td>{{ row.products | listToString }}</td>
                                        <td>
                                            <i
                                                class="tim-icons icon-trash-simple cursor-pointer"
                                                :idx="i"
                                                :data_source_name="row.data_source_name"
                                                @click="deleteDataSource($event)"
                                            />
                                        </td>
                                    </v-tr>
                                </tbody>
                            </v-table>
                        </div>
                    </div>
                </card>
            </div>
            <div class="col">
                <card type="card">
                    <data-source-detail
                        v-if="getSelectedItem() != null"
                        :dataSource="getSelectedItem()"
                        :allDataSources="doc.data_sources"
                        :dqHelpText="dqHelpText"
                        :dsHelpText="dsHelpText"
                        :prevDataSourceQuality="prevDataSourceQuality"
                        :navigateItem="navigateItem"
                    ></data-source-detail>
                </card>
            </div>
        </div>
    </div>
</template>
<script>
import DataSourceDetail from './DataSourceDetail';
import Icons from '@/components/Icons';
import jsyaml from 'js-yaml';
import moment from 'moment';
import constants from '@/constants';
import { pageMixin } from '../mixins/PageMixins.js';
import { navigateMixins } from '../mixins/NavigateMixins.js';
import { notificationMixin } from '../mixins/NotificationMixins.js';
import _ from 'lodash';

export default {
    name: 'data-sources-page',
    data() {
        return {
            filters: {
                filter: {
                    value: '',
                    keys: ['data_source_name', 'date_registered', 'products']
                }
            },
            prevDataSourceQuality: [],
            data_columns: ['data_source_name', 'date_registered', 'products'],
            dqFileToRender: 'https://raw.githubusercontent.com/wiki/rabobank-cdc/DeTTECT/Data-quality-scoring.md',
            dqHelpText: null,
            dsFileToRender: 'https://raw.githubusercontent.com/wiki/rabobank-cdc/DeTTECT/YAML-administration-data-sources.md',
            dsHelpText: null,
            emptyDataSourceObject: constants.YAML_OBJ_DATA_SOURCES
        };
    },
    mixins: [pageMixin, navigateMixins, notificationMixin],
    components: {
        DataSourceDetail,
        Icons
    },
    created: function() {
        this.preloadMarkDown();
    },
    methods: {
        readFile(event) {
            // Loads and checks the file content
            try {
                let yaml_input = jsyaml.load(event.result);

                if (yaml_input['file_type'] == 'data-source-administration') {
                    if (yaml_input['version'] != constants.YAML_DATASOURCES_VERSION) {
                        this.notifyDanger('Invalid file version', 'The version of the YAML file is not supported by this version of the Editor.');
                    } else {
                        ///////////////////////////////////////////////
                        // Health checks before assignment to this.doc:
                        ///////////////////////////////////////////////

                        // Fix missing or empty platform:
                        if (yaml_input.platform == undefined || yaml_input.platform == null) {
                            yaml_input.platform = [];
                        }

                        // Fix a single platform string to list
                        if (typeof yaml_input.platform == 'string') {
                            yaml_input.platform = [yaml_input.platform];
                        }

                        // Only use valid platform values (in right casing):
                        let valid_platforms = [];
                        for (let i = 0; i < yaml_input.platform.length; i++) {
                            if (this.platforms.indexOf(yaml_input.platform[i]) < 0) {
                                let p = yaml_input.platform[i].toLowerCase();
                                if (Object.keys(constants.PLATFORM_CONVERSION).indexOf(p) >= 0) {
                                    valid_platforms.push(constants.PLATFORM_CONVERSION[p]);
                                } else {
                                    this.notifyDanger('Invalid value', 'Invalid value for platform was found in the YAML file and was removed.');
                                }
                            } else {
                                valid_platforms.push(yaml_input.platform[i]);
                            }
                        }
                        yaml_input.platform = valid_platforms;

                        // Fix missing/invalid fields: 'products', available_for_data_analytics, data_quality
                        for (let i = 0; i < yaml_input.data_sources.length; i++) {
                            if (yaml_input.data_sources[i].products == undefined) {
                                yaml_input.data_sources[i].products = [];
                            }

                            if (yaml_input.data_sources[i].available_for_data_analytics == undefined) {
                                yaml_input.data_sources[i].available_for_data_analytics = false;
                            }

                            if (typeof yaml_input.data_sources[i].available_for_data_analytics != 'boolean') {
                                yaml_input.data_sources[i].available_for_data_analytics = false;
                            }

                            if (yaml_input.data_sources[i].data_quality == undefined) {
                                yaml_input.data_sources[i].data_quality = {
                                    device_completeness: 0,
                                    data_field_completeness: 0,
                                    timeliness: 0,
                                    consistency: 0,
                                    retention: 0
                                };
                            }

                            yaml_input.data_sources[i].data_quality.device_completeness = this.fixSDataQualityScore(
                                yaml_input.data_sources[i].data_quality.device_completeness
                            );
                            yaml_input.data_sources[i].data_quality.data_field_completeness = this.fixSDataQualityScore(
                                yaml_input.data_sources[i].data_quality.data_field_completeness
                            );
                            yaml_input.data_sources[i].data_quality.timeliness = this.fixSDataQualityScore(
                                yaml_input.data_sources[i].data_quality.timeliness
                            );
                            yaml_input.data_sources[i].data_quality.consistency = this.fixSDataQualityScore(
                                yaml_input.data_sources[i].data_quality.consistency
                            );
                            yaml_input.data_sources[i].data_quality.retention = this.fixSDataQualityScore(
                                yaml_input.data_sources[i].data_quality.retention
                            );
                        }

                        // For the following fields it's not a problem is they are missing because the GUI solves/handles this properly:
                        // - date_registered. Also invalid values are handled correctly.
                        // - date_connected. Also invalid values are handled correctly.
                        // - comment

                        this.doc = yaml_input;
                        this.filename = this.selected_filename;
                        this.filters.filter.value = '';
                        while (this.selectedRow != null && this.selectedRow.length > 0) {
                            this.selectedRow.pop();
                        }

                        // Fix the date to be in the correct date format (YYY-MM-DD):
                        for (let i = 0; i < this.doc.data_sources.length; i++) {
                            let dr = this.doc.data_sources[i]['date_registered'];
                            let dv = this.doc.data_sources[i]['date_connected'];
                            if (dr != null) {
                                this.doc.data_sources[i]['date_registered'] = moment(dr, 'DD/MM/YYYY').format('YYYY-MM-DD');
                            }
                            if (dv != null) {
                                this.doc.data_sources[i]['date_connected'] = moment(dv, 'DD/MM/YYYY').format('YYYY-MM-DD');
                            }
                        }

                        this.prevDataSourceQuality = [];
                        this.fileChanged = false;
                        this.setWatch();

                        // Reset the file reader for Chrome, so that it will be possible to load the same file again:
                        document.getElementById('dsFileReader').value = null;
                    }
                } else {
                    this.notifyInvalidFileType(this.selected_filename);
                }
            } catch (e) {
                // alert(e);
                this.notifyInvalidFileType(this.selected_filename);
            }
        },
        newFile() {
            this.filename = 'data-sources-new.yaml';
            this.selected_filename = 'data-sources-new.yaml';
            this.doc = _.cloneDeep(constants.YAML_OBJ_NEW_DATA_SOURCES_FILE);
            this.selectedRow.pop();
            this.deletedRows = [];
            this.fileChanged = false;
            this.setWatch();
        },
        fixSDataQualityScore(v) {
            if (v == undefined) {
                return 0;
            } else if (v < 0) {
                return 0;
            } else if (v > 5) {
                return 5;
            } else if (typeof v == 'number') {
                return v;
            } else {
                return 0;
            }
        },
        cleanupBeforeDownload() {
            // empty function. must be here to make downloadYaml() work for every page
        },
        convertBeforeDownload(newDoc) {
            // Convert the date (which is a string in the GUI) to a real Date object in the YAML file
            for (let i = 0; i < newDoc.data_sources.length; i++) {
                if (newDoc.data_sources[i]['date_registered'] != null) {
                    newDoc.data_sources[i]['date_registered'] = new Date(newDoc.data_sources[i]['date_registered']);
                }
                if (newDoc.data_sources[i]['date_connected'] != null) {
                    newDoc.data_sources[i]['date_connected'] = new Date(newDoc.data_sources[i]['date_connected']);
                }
            }
        },
        deleteDataSource(event) {
            this.deleteItem(event, 'data_sources', 'data_source_name', 'Data source', this.recoverDeletedDataSource);
        },
        recoverDeletedDataSource(data_source_name) {
            this.recoverDeletedItem('data_sources', data_source_name);
        },
        preloadMarkDown() {
            // Preload the data quality help text from Github
            this.dqHelpText = 'Loading the help content...';
            this.$http.get(this.dqFileToRender).then(
                (response) => {
                    // remove links to other wiki pages
                    this.dqHelpText = response.body.replace(/\[(.+)\](\([#\w-]+\))/gm, '$1');
                },
                // eslint-disable-next-line no-unused-vars
                (response) => {
                    this.dqHelpText = 'An error occurred while loading the help content.';
                }
            );

            this.dsHelpText = 'Loading the help content...';
            this.$http.get(this.dsFileToRender).then(
                (response) => {
                    this.dsHelpText = response.body.replace(/\[(.+)\](\([#\w-]+\))/gm, '$1'); // remove links to other wiki pages
                    this.dsHelpText = this.dsHelpText.match(/## Data source object((.*|\n)*)/gim, '$1')[0];
                    this.dsHelpText = this.dsHelpText.replace(/^## Data source object/gim, '');
                    this.dsHelpText = this.dsHelpText.replace(/^## .+((.*|\n)*)/gim, '');
                },
                // eslint-disable-next-line no-unused-vars
                (response) => {
                    this.dsHelpText = 'An error occurred while loading the help content.';
                }
            );
        },
        notifyInvalidFileType(filename) {
            this.notifyDanger('Invalid YAML file type', "The file '" + filename + "' is not a valid data source administration file.");
        },
        readLogFiles(event) {
            let files = event.target.files;
            let promises = [];
            let text = [];

            for (let i = 0; i < files.length; i++) {
                promises.push(files.item(i).text());
            }

            Promise.all(promises).then(texts => {
                text = texts;
                this.readXML(text);
            });
        },
        readXML(XML_logs) {
            let MainEID=[];

            for (let i=0; i<XML_logs.length; i++){
                let EID_list = [];
                let parser = new DOMParser();
                let xmlDoc = parser.parseFromString(XML_logs[i],"text/xml");

                //counting the number of event ids in xml
                let count = (XML_logs[i].match(/<EventID>/g)).length;

                for (let j=0; j<count; j++){
                    let EID = xmlDoc.getElementsByTagName("EventID")[j].childNodes[0].nodeValue; 
                    EID_list.push(EID);
                }

                MainEID.push(EID_list);  
            }
            console.log(MainEID);
        },
        fillDocument(mappings) {
            mappings.forEach(doc => {
                doc.forEach(source => {
                    let obj = YAML_OBJ_DATA_SOURCES;
                    obj.data_source_name = source;

                    this.doc.data_sources.push(obj);
                });
            });
        }
    },
    filters: {
        listToString: function(value) {
            if (Array.isArray(value)) {
                return value.join(', ');
            } else {
                return value;
            }
        }
    }
};
</script>

<style></style>
