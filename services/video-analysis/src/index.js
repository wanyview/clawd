/**
 * 视频分析服务
 * 用于分析下载的视频文件
 */

const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const VIDEO_DIR = path.join(process.env.APPDATA || '', '.openclaw', 'media', 'inbound');

// 检查 ffmpeg 是否可用
function checkFFmpeg() {
  try {
    execSync('ffmpeg -version', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

// 获取视频信息
function getVideoInfo(videoPath) {
  try {
    const output = execSync(`ffprobe -v quiet -print_format json -show_format -show_streams "${videoPath}"`, {
      encoding: 'utf8'
    });
    return JSON.parse(output);
  } catch (error) {
    return { error: '无法获取视频信息', details: error.message };
  }
}

// 截取帧截图
function extractFrame(videoPath, timestamp = '00:00:01', outputPath = null) {
  if (!outputPath) {
    outputPath = path.join(VIDEO_DIR, 'screenshots', `${path.basename(videoPath, path.extname(videoPath))}_${timestamp.replace(/:/g, '-')}.jpg`);
  }
  
  fs.ensureDirSync(path.dirname(outputPath));
  
  try {
    execSync(`ffmpeg -ss "${timestamp}" -i "${videoPath}" -vframes 1 -q:v 2 "${outputPath}" -y`, {
      stdio: 'ignore'
    });
    return { success: true, path: outputPath };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 生成视频缩略图
function generateThumbnail(videoPath, timestamp = '00:00:01') {
  return extractFrame(videoPath, timestamp);
}

// 视频转音频（用于语音转文字）
function extractAudio(videoPath, outputPath = null) {
  if (!outputPath) {
    outputPath = path.join(VIDEO_DIR, 'audio', `${path.basename(videoPath, path.extname(videoPath))}.mp3`);
  }
  
  fs.ensureDirSync(path.dirname(outputPath));
  
  try {
    execSync(`ffmpeg -i "${videoPath}" -vn -acodec libmp3lame -q:a 2 "${outputPath}" -y`, {
      stdio: 'ignore'
    });
    return { success: true, path: outputPath };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 列出所有视频
function listVideos() {
  fs.ensureDirSync(VIDEO_DIR);
  const files = fs.readdirSync(VIDEO_DIR);
  return files
    .filter(f => ['.mov', '.mp4', '.avi', '.mkv', '.webm'].includes(path.extname(f).toLowerCase()))
    .map(f => ({
      name: f,
      path: path.join(VIDEO_DIR, f),
      size: fs.statSync(path.join(VIDEO_DIR, f)).size
    }));
}

module.exports = {
  checkFFmpeg,
  getVideoInfo,
  extractFrame,
  generateThumbnail,
  extractAudio,
  listVideos
};
