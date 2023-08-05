# gRPC stac-client-python
### What is this Good for
This is a generic python client for accessing gRPC STAC service to find geospatial asset metadata using query filters. 

#### A gRPC Spatio Temporal Asset Catalog python client 
This python client library is used for conneting to a gRPC enabled STAC service. STAC items and STAC requests are Protocol Buffers (protobuf) instead of traditional JSON.

Definition of STAC from https://stacspec.org/:
> The SpatioTemporal Asset Catalog (STAC) specification provides a common language to describe a range of geospatial information, so it can more easily be indexed and discovered.  A 'spatiotemporal asset' is any file that represents information about the earth captured in a certain space and time.

Definition of gRPC from https://grpc.io
> gRPC is a modern open source high performance RPC framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication. It is also applicable in last mile of distributed computing to connect devices, mobile applications and browsers to backend services.

Definitions of Protocol Buffers (protobuf) from https://developers.google.com/protocol-buffers/
> Protocol buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data – think XML, but smaller, faster, and simpler. You define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

This client library allows for searching Spatio Temporal Asset Catalog information through complex queries.

### Setup
Grab it from [pip](https://pypi.org/project/nsl.stac/):
```bash
pip install nsl.stac
```

Install it from source:
```bash
pip install -r requirements.txt
python setup.py install
```

#### Environment Variables
There are a few environment variables that the stac-client-python library relies on for accessing the STAC service:

- STAC_SERVICE, the address of the stac service you connect to (defaults to "localhost:10000")
- AUTH
- BEARER

## Protocol Buffer and gRPC API

## Differences between gRPC+Protobuf STAC and OpenAPI+JSON STAC
If you are already familiar with STAC, you'll need to know that STAC + gRPC + Protobuf is slightly different from the JSON definitions. 

JSON is naturally a flexible format and with linters you can force it to adhere to rules. Protobuf is a strict data format and that required a few differences between the JSON stac specification and the protobuf specification:

### StacItem
A Stac Item contains the spatial extent, the datetime of observation, the downloadable assets of the item, and other metadata uniquely identifying the data. 
 
For a summary of the protobuf `StacItem` visit the protobuf documentation [here](https://geo-grpc.github.io/api/#epl.protobuf.StacItem).

To understand where much of the inspiration for the protobuf `StacItem`, check out the summary of the JSON specification (the guide and inspiration for this protobuf version) can be found [here](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#item-fields).

|  Field Name 	| Stac Protobuf Type                                                         	| Stac JSON Type 	| Description 	|   	|
|-------------	|----------------------------------------------------------------------------	|----------------	|-------------	|---	|
| id          	| [string](https://geo-grpc.github.io/api/#string)                           	|                	|             	|   	|
| type        	|                                                                            	|                	|             	|   	|
| geometry    	| [GeometryData](https://geo-grpc.github.io/api/#epl.protobuf.GeometryData)  	|                	|             	|   	|
| bbox        	| [EnvelopeData](https://geo-grpc.github.io/api/#epl.protobuf.EnvelopeData)  	|                	|             	|   	|
| properties  	| [google.protobuf.Any](https://geo-grpc.github.io/api/#google.protobuf.Any) 	|                	|             	|   	|
| links       	|                                                                            	|                	|             	|   	|
| assets      	|                                                                            	|                	|             	|   	|
| collection  	|                                                                            	|                	|             	|   	|

| Field Name | Stac JSON Type                                                               | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| id         | string                                                                     | **REQUIRED.** Provider identifier. As most geospatial assets are already defined by some identification scheme by the data provider it is recommended to simply use that ID. Data providers are advised to include sufficient information to make their IDs globally unique, including things like unique satellite IDs. |
| type       | string                                                                     | **REQUIRED.** Type of the GeoJSON Object. MUST be set to `Feature`. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Specified in Longitude/Latitude based on EPSG:4326. |
| bbox       | [number]                                                                   | **REQUIRED.** Bounding Box of the asset represented by this item. Specified in Longitude/Latitude based on EPSG:4326 - first two numbers are longitude and latitude of lower left corner, followed by longitude and latitude of upper right corner. This field enables more naive clients to easily index and search geospatially. Most software can easily generate them for footprints. STAC compliant APIs are required to compute intersection operations with the item's geometry field, not its bbox. |
| properties | Properties Object                                                          | **REQUIRED.** A dictionary of additional metadata for the item. |
| links      | [Link Object]                                                              | **REQUIRED.** List of link objects to resources and related URLs. A link with the `rel` set to `self` is required. |
| assets     | Map<string, Asset Object>                                                  | **REQUIRED.** Dictionary of asset objects that can be downloaded, each with a unique key. Some pre-defined keys are listed in the chapter 'Asset types'. |
| collection | string                                                                     | The `id` of the STAC Collection this Item references to (see `collection` relation type below). This field is *required* if such a relation type is present. This field provides an easy way for a user to search for any Items that belong in a specified Collection. |

 
The STAC item for a specific observation of data is summarized in the [stac repo](github.com/radiantearth/stac-spec/item-spec/README.md).

is represented by a protobuf message in the stac client.  

#### Google DataTypes vs native data types
   - TimeStamp
   - FloatValue

### StacRequest


### JSON STAC Compared with Protobuf STAC
|  Field Name 	| Stac Protobuf Type                                                                                                       	| Stac JSON Type                                                             	|
|-------------	|--------------------------------------------------------------------------------------------------------------------------	|----------------------------------------------------------------------------	|
| id          	| [string](https://geo-grpc.github.io/api/#string)                                                                         	| string                                                                     	|
| type        	| NA                                                                                                                       	| string                                                                     	|
| geometry    	| [GeometryData](https://geo-grpc.github.io/api/#epl.protobuf.GeometryData)                                                	| [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) 	|
| bbox        	| [EnvelopeData](https://geo-grpc.github.io/api/#epl.protobuf.EnvelopeData)                                                	| [number]                                                                   	|
| properties  	| [google.protobuf.Any](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/any.proto)                                               	| Properties Object                                                          	|
| links       	| NA                                                                                                                       	| [Link Object]                                                              	|
| assets      	| [StacItem.AssetsEntry](https://geo-grpc.github.io/api/#epl.protobuf.StacItem.AssetsEntry)                                	| Map                                                                        	|
| collection  	| [string](https://geo-grpc.github.io/api/#string)                                                                         	| string                                                                     	|
| title       	| [string](https://geo-grpc.github.io/api/#string)                                                                         	| Inside Properties                                                          	|
| datetime    	| [google.protobuf.Timestamp](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/timestamp.proto) 	| Inside Properties                                                          	|
| observation 	| [google.protobuf.Timestamp](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/timestamp.proto) 	| Inside Properties                                                          	|
| processed   	| [google.protobuf.Timestamp](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/timestamp.proto) 	| Inside Properties                                                          	|
| updated     	| [google.protobuf.Timestamp](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/timestamp.proto) 	| Inside Properties                                                          	|
| duration    	| [google.protobuf.Duration](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/duration.proto)   	| Inside Properties                                                          	|
| eo          	| [Eo](https://geo-grpc.github.io/api/#epl.protobuf.Eo)                                                                    	| Inside Properties                                                          	|
| sar         	| [Sar](https://geo-grpc.github.io/api/#epl.protobuf.Sar)                                                                  	| Inside Properties                                                          	|
| landsat     	| [Landsat](https://geo-grpc.github.io/api/#epl.protobuf.Landsat)                                                          	| Inside Properties                                                          	|