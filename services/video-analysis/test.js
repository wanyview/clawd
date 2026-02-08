/**
 * 视频分析测试
 */

const { listVideos, getVideoInfo, extractFrame, checkFFmpeg } = require('./src/index.js');

console.log('🎬 视频分析服务测试\n');

console.log('✅ FFmpeg 可用:', checkFFmpeg());

console.log('\n📁 视频列表:');
const videos = listVideos();
console.log(`找到 ${videos.length} 个视频文件`);

if (videos.length > 0) {
  const video = videos[0];
  console.log(`\n📹 当前视频: ${video.name}`);
  console.log(`   大小: ${(video.size / 1024 / 1024).toFixed(2)} MB`);
  
  console.log('\n🔍 视频信息:');
  const info = getVideoInfo(video.path);
  if (info.streams) {
    const stream = info.streams[0];
    console.log(`   编码: ${stream.codec_name}`);
    console.log(`   分辨率: ${stream.width}x${stream.height}`);
    console.log(`   时长: ${parseFloat(info.format.duration).toFixed(1)} 秒`);
  } else {
    console.log(JSON.stringify(info, null, 2));
  }
  
  console.log('\n🖼️ 截取帧测试:');
  const frame = extractFrame(video.path, '00:00:01');
  console.log(frame);
}
